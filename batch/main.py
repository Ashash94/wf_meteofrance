from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from meteo import connect_bdd, get_key_data, fetch_data_table_mf, delete_data_forecast
from city_list import open_cities_json, create_table_cities, fill_table_cities, check_expected_city_in_db, get_cities_list

cur, conn = connect_bdd()

city_file = open_cities_json()
create_table_cities(cur, conn)
fill_table_cities(cur, conn,city_file)
cities_list = get_cities_list(cur)
fetch_data_table_mf(cur, conn, cities_list)

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

@app.get("/test/{prompt}", description= "test")
async def test(prompt):
    print("chat", prompt)
    return {"resp": prompt}

@app.get("/forecast_mf/{city}", description="Return the latest forecasts from MeteoFrance for a city and a date defined by the user.The date format is DD-MM-YYYY, forecasts are available from D-Day to D+9")

async def forecast_mf(city, date_str):
    check_expected_city_in_db(city, cur, conn)
    weather_data = get_key_data(cur,city, date_str)
    if weather_data is None:
        print("Pas de donnée pour la ville demandée.")
    else:
        print(weather_data)
        return weather_data

if __name__ == "__main__":
    uvicorn.run(app,host= "0.0.0.0", port=9999)