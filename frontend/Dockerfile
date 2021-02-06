# Stage: build

FROM node:14-alpine as builder

WORKDIR /app

COPY package.json ./
COPY ./ ./

RUN npm install

RUN npm run build

# Stage: publish

FROM nginx:1.18.0

RUN rm -rf /usr/share/nginx/html

COPY --from=builder /app/dist /usr/share/nginx/html
