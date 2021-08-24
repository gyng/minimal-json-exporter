FROM python:3.9.6-alpine3.14

WORKDIR /app

RUN pip install flask

COPY app.py /app/app.py

CMD ["python", "app.py"]
