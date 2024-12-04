FROM python:3.11-slim-buster

LABEL authors="Abhay"

WORKDIR /blog-app

COPY requirements.txt /blog-app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /blog-app

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]