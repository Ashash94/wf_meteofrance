FROM python:3.11-alpine

RUN apk add --no-cache postgresql-dev

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn psycopg2-binary meteofrance_api schedule

EXPOSE 5432 9999

CMD ["python", "main.py"]
