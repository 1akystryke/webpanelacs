# building stage
FROM node:18 AS builder

WORKDIR /app

COPY web-app/package*.json ./
RUN npm install webpack-plugin-vuetify@^3.1.0 && npm install

COPY web-app/. .
RUN npm run build

# deployment stage
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y supervisor && pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY vue  ./vue/
COPY --from=builder /app/dist ./static/
COPY core ./core/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


EXPOSE 5000

CMD ["/usr/bin/supervisord", "-n"]
