# stock-forecaster
Forecast stock prices using yfinances, fbprophet, scrapy and fastAPI.

The stock list is scraped using a Scrapy spider and used as input options for the user.
A user can choose an existing stock from the prefilled stock names and symbols.

The fastAPI app will handle the input, get the stock history using yfinnance and do the necessary transformation for the fbprophet model input.
A new model will be created using fbprophet and it will forecast a number of x values (5Y as default).

Everything will be rendered using Jinja, Chartjs and picocss.

The project is live at https://stock-forecaster.techwetrust.com/

![Landing page](https://iili.io/HEdEiCv.md.png)
![Result page](https://iili.io/HEdGFF2.md.png)
