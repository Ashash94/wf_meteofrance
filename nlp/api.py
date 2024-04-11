from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from nlp.nlp import generate_forecast_text, get_audio

# Fonction pour jouer le jingle (à compléter et à ajouter dans le front)

# def play_jingle():
#     os.startfile("../mf_api/data/jingle_meteo.mp3")
# play_jingle()

def handle_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )
    return app

app = handle_cors(FastAPI())

# @app.get("/forecast/{city}", response_class=HTMLResponse)
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="item.html", context={"id": id}
#     )

@app.get("/test/{prompt}", description= "test")
async def test(prompt):
    print("chat", prompt)
    return {"resp": prompt}

@app.get("/gen_text/{prompt}", description="Generate a forecast audio based on weather input")
async def gen_text(prompt):
    fc_text = generate_forecast_text(prompt)
    print(fc_text)
    final_fc = get_audio(fc_text)
    return final_fc

if __name__ == "__main__":
    uvicorn.run(app,host= "0.0.0.0", port=8000)