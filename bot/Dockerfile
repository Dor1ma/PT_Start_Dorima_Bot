FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r bot/requirements.txt

CMD ["python", "/app/bot/main.py"]
