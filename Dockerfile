FROM python:3.9-alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./

ENV PYTHONDONTWRITEBYTECODE yes
ENV PYTHONUNBUFFERED yes

ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["main.py"]
