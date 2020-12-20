# Stage: build

FROM python:3.9-alpine as builder

# TODO Review what's really needed
RUN apk add --no-cache \
  build-base curl wget make git

WORKDIR /app

RUN pip install \
  mkdocs==1.1.2 \
  mkdocs-material==6.1.7

COPY ./mkdocs.yml ./
COPY ./*.md ./
COPY ./docs ./docs

RUN mkdocs build

# Stage: pack

FROM nginx:1.18-alpine

COPY --from=builder /app/site /usr/share/nginx/html
