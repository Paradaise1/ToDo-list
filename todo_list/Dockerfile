FROM python:3.11.4

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
COPY entrypoint.sh .
EXPOSE 8000

CMD ["sh", "entrypoint.sh"]