from fastapi import FastAPI, Request
from starlette.background import BackgroundTask
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi import BackgroundTasks
from runner import get_history
from predict import is_stock_ready, run_forecaster
from tools import load_data, get_data, resample_df
from fastapi.templating import Jinja2Templates
from pandas import DataFrame, read_pickle

data: DataFrame = load_data()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


@app.get("/suggestions")
async def root(q: str):
    return get_data(data, q)


@app.get("/names")
async def get_stock_names():
    return data.to_dict('records')


@app.get("/stock/{symbol}")
async def stock_data(symbol: str):
    history = get_history(symbol=symbol)
    return {"data": history}


@app.get("/forecast")
async def forecast(symbol: str, background_tasks: BackgroundTasks):
    task = BackgroundTask(run_forecaster, symbol)
    if not is_stock_ready(symbol) and task not in background_tasks.tasks:
        background_tasks.add_task(run_forecaster, symbol)
        return {'created': True}
    return {'created': False}


@app.get("/result/{symbol}", response_class=HTMLResponse)
async def show_result(request: Request, symbol: str):
    extra_resample = True
    def prepare_df(df):
        df['ds'] = df['ds'].apply(lambda x: str(x.isoformat()))
        return df.to_dict('records')

    def prepare_chart_data(items, label_key, value_key):
        return [dict(x=item[label_key], y=item[value_key]) for item in items]

    history = read_pickle(f'data/{symbol}-history')
    forecast = read_pickle(f'data/{symbol}-forecast')
    if extra_resample:
        chart_history = resample_df(history.copy(), 'ds')
        chart_forecast = resample_df(forecast.copy(), 'ds')
    else:
        chart_history, chart_forecast = history.copy(), forecast.copy()
    print(chart_forecast.keys)
    chart_history = prepare_df(chart_history)
    chart_forecast = prepare_df(chart_forecast)
    history = prepare_chart_data(chart_history, 'ds', 'y')
    trend = prepare_chart_data(chart_forecast, 'ds', 'yhat')
    lower = prepare_chart_data(chart_forecast, 'ds', 'yhat_lower')
    upper = prepare_chart_data(chart_forecast, 'ds', 'yhat_upper')

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "history": history, "trend": trend, "lower":lower, "upper": upper}
    )


@app.get("/stock/{symbol}/ready")
async def stock_ready(symbol: str, request: Request):
    is_ready = is_stock_ready(symbol)
    url = "" if not is_ready else request.url_for('show_result', symbol=symbol)
    return {"is_ready": is_ready, "url_to_redirect": url}
