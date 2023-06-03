# Stage: build

FROM node:16-alpine as builder

WORKDIR /app

COPY package.json ./
COPY ./ ./

RUN npm install

# hadolint ignore=DL3059
RUN npm run build

# Stage: publish

FROM nginx:1.18.0

RUN rm -rf /usr/share/nginx/html

COPY --from=builder /app/dist /usr/share/nginx/html
