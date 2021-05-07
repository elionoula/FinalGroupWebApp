FROM python:3.8

EXPOSE 5000

WORKDIR /pythonlogin

COPY requirements.txt /pythonlogin
RUN pip install  -r requirements.txt --upgrade pip

COPY . /pythonlogin

CMD python app.py