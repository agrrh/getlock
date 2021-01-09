FROM python:3.9-alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./config.example.yml ./
COPY ./lib ./lib
COPY ./getlock.py ./

ENV PYTHONDONTWRITEBYTECODE yes
ENV PYTHONUNBUFFERED yes

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--threads", "4", "--max-requests", "1000", "getlock:app"]
