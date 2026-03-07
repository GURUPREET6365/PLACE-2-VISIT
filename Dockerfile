FROM python:3.14.3

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port $PORT"]