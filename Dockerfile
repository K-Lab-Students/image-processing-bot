FROM python:3.10-alpine

RUN apk update && apk add --no-cache \
    build-base \
    opencv-dev \
    py3-opencv \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
