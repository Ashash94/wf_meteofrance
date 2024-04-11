import requests
import base64
from gtts import gTTS
# import os (pour le jingle)

from config import LLM_URL, API_KEY
    
def generate_forecast_text(weather_data:str) -> str:
    context = "Parle comme Evelyne Dhéliat, la présentatrice de TF1"
    
    payload = {
    "response_as_dict": True,
    "temperature": 0.2,
    "max_tokens": 200,
    "providers": "openai",
    "text": context + weather_data,
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(LLM_URL, json=payload, headers=headers)
    # Vérifier si valide
    if response.status_code == 200:
        response_json = response.json()
        text_forecast = response_json.get('openai', {}).get('generated_text', None)
        if text_forecast:
            return text_forecast
        else:
            print("Erreur: Le texte généré n'a pas été trouvé dans la réponse.")
            return None
    else:
        print(f"Erreur:{response.status_code} - {response.text}")
        return None
    
def get_audio(text_forecast):
        tts = gTTS(text=text_forecast, lang='fr')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        return encoded_audio


