FROM python:3.7
ADD src/stocks_grabber/requirements.txt /

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir pystan==2.19.1.1
RUN pip install --no-cache-dir fbprophet==0.7.1
RUN pip install --no-cache-dir "numpy<1.24"
RUN pip install --no-cache-dir -r requirements.txt
ADD src/stocks_grabber /
CMD ["uvicorn", "api:app", "--host", "0.0.0.0"]