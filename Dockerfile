FROM python:3.13.3-slim

ENV PYTHONDONTWRITEBYTECODE yes

WORKDIR /app

COPY requires.txt requires.txt
RUN pip install -r requires.txt

COPY bot.py bot.py
