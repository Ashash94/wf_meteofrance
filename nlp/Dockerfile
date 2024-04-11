FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn pyttsx3 requests gTTS

EXPOSE 8000

CMD ["python", "api.py"]
