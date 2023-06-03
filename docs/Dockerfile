# Stage: build

FROM python:3.9-alpine as builder

# TODO Review what's really needed
RUN apk add --no-cache \
  build-base=~0.5 \
  curl=~8.1 \
  git=~2.40 \
  make=~4.4 \
  wget=~1.21

WORKDIR /app

RUN pip install --no-cache-dir \
  mkdocs==1.1.2 \
  mkdocs-material==6.1.7 \
  jinja2==3.0.3

COPY ./mkdocs.yml ./
COPY ./*.md ./
COPY ./docs ./docs

RUN mkdocs build

# Stage: pack

FROM nginx:1.18-alpine

COPY --from=builder /app/site /usr/share/nginx/html
