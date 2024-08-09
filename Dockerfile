FROM python:3.10-alpine

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install fastapi uvicorn motor

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]