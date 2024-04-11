import psycopg2
from meteofrance_api import MeteoFranceClient
from datetime import datetime, timedelta


from config import BDD_DBNAME, BDD_HOST, BDD_PORT, BDD_USER, BDD_PW

def connect_bdd():
    conn = psycopg2.connect(
        dbname = BDD_DBNAME,
        user = BDD_USER,
        password = BDD_PW,
        host = BDD_HOST,
        port = BDD_PORT
    )
    cur = conn.cursor()
    print('la connexion est établie')
    return cur, conn

def get_weather_forecasts(postcode: str):
    try:
        client = MeteoFranceClient()

        list_places = client.search_places(postcode)

        if not list_places:
            return {"error": "No places found for the specified postal code."}

        my_place = list_places[0]
        fc = client.get_forecast_for_place(my_place)
        daily_fc = fc.forecast
        return daily_fc

    except Exception as e:
        print(e)
        return {"error": str(e)}

# Création de la table
def create_table_forecasts(cur, conn):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS mf_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            postCode VARCHAR(5),
            date VARCHAR(22),
            temp FLOAT,
            windchill FLOAT,
            hum INTEGER,
            seaLvl FLOAT,
            windSpeed VARCHAR(2),
            windDirection VARCHAR(20),
            rain INTEGER,
            rainTier VARCHAR(3),
            snow INTEGER,
            snowTier VARCHAR(3),
            clouds INTEGER,
            descr VARCHAR(70),
            update_dt VARCHAR(22)
        )
        """
    )
    conn.commit()

# Fonctions pour formater l'heure
    
def format_forecast_dt(timestamp: int) -> str :
    formatted_dt = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S")
    return formatted_dt

def format_update_dt():
    update_dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return update_dt

# Fonctions pour extraire les bonnes valeurs pour la pluie et la neige
def format_rain(wf):
    rain = list(wf["rain"].values())[0]
    return rain

def format_rain_tier(wf):
    rain_tier = list(wf["rain"].keys())[0]
    return rain_tier

def format_snow(wf):
    snow = list(wf["snow"].values())[0]
    return snow

def format_snow_tier(wf):
    snow_tier = list(wf["rain"].keys())[0]
    return snow_tier

def fetch_data_table_mf(cur, conn, cities_list):
    for c in cities_list:
        city_label = c['city']
        postcode = c['postcode']
        weather_forecasts = get_weather_forecasts(postcode)
        
        if isinstance(weather_forecasts, dict) and "error" in weather_forecasts:
            # Gère les erreurs API
            print(f"Aucune donnée météo trouvée pour {city_label} car: {weather_forecasts['error']}")
            continue
        
        if not weather_forecasts:
            print(f"Pas de prévision disponible pour la ville {city_label}")
            continue
        
        for wf in weather_forecasts:
            if isinstance(wf, dict):
                timestamp = int(wf['dt'])
                date = format_forecast_dt(timestamp)
                temp = wf["T"]["value"]
                windchill = wf["T"]["windchill"]
                hum = wf["humidity"]
                seaLvl = wf["sea_level"]
                windSpeed = wf["wind"]["speed"]
                windDirection = wf["wind"]["icon"]
                rain = format_rain(wf)
                rain_tier = format_rain_tier(wf)
                snow = format_snow(wf)
                snow_tier = format_snow_tier(wf)
                clouds = wf["clouds"]
                desc = wf["weather"]["desc"]
                update_dt = format_update_dt()

                cur.execute(
                    """
                    INSERT INTO mf_data (city, postCode, date, temp, windchill, hum, seaLvl, windSpeed, windDirection, rain, rainTier, snow, snowTier, clouds, descr, update_dt) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (city_label, postcode, date, temp, windchill, hum, seaLvl, windSpeed, windDirection, rain, rain_tier, snow, snow_tier, clouds, desc, update_dt)
                )
                conn.commit()
                print(f"Les données météo pour {city_label} ont bien été ajoutées.")
            else:
                print(f"Aucune donnée météo disponible pour {city_label}")
                          
def data_new_city_mf(cur, conn, city, postcode):

    weather_forecasts = get_weather_forecasts(city)
    
    if isinstance(weather_forecasts, dict) and "error" in weather_forecasts:
        # Gère les erreurs API
        print(f"Aucune donnée météo trouvée pour {city} car: {weather_forecasts['error']}")
        return None
    
    if not weather_forecasts:
        print(f"Pas de prévision disponible pour la ville {city}")
        return None
    
    for wf in weather_forecasts:
        if isinstance(wf, dict):
            timestamp = int(wf['dt'])
            date = format_forecast_dt(timestamp)
            temp = wf["T"]["value"]
            windchill = wf["T"]["windchill"]
            hum = wf["humidity"]
            seaLvl = wf["sea_level"]
            windSpeed = wf["wind"]["speed"]
            windDirection = wf["wind"]["icon"]
            rain = format_rain(wf)
            rain_tier = format_rain_tier(wf)
            snow = format_snow(wf)
            snow_tier = format_snow_tier(wf)
            clouds = wf["clouds"]
            desc = wf["weather"]["desc"]
            update_dt = format_update_dt()
            # Insérer les données dans la table
            cur.execute(
                """
                INSERT INTO mf_data (city, postCode, date, temp, windchill, hum, seaLvl, windSpeed, windDirection, rain, rainTier, snow, snowTier, clouds, descr, update_dt) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (city, postcode, date, temp, windchill, hum, seaLvl, windSpeed, windDirection, rain, rain_tier, snow, snow_tier, clouds, desc, update_dt)
            )
            
            # Commit des modifications dans la base de données
            conn.commit()
            print(f"Les données météo pour {city} ont bien été ajoutées.")
        else:
            print(f"Aucune donnée météo disponible pour {city}")
            
def get_key_data(cur, city, date_str):

    # Requête pour récupérer la température maximale
    query_max_temp = """
        SELECT MAX(temp) FROM mf_data WHERE city = %s AND date::date = %s
    """
    cur.execute(query_max_temp, (city, date_str))
    max_temp = cur.fetchone()[0]
    
    # Requête pour récupérer la température minimale
    query_min_temp = """
        SELECT MIN(temp) FROM mf_data WHERE city = %s AND date::date = %s
    """
    cur.execute(query_min_temp, (city, date_str))
    min_temp = cur.fetchone()[0]
    
    # Requête pour récupérer la pluie
    query_max_rain = """
        SELECT MAX(rain) FROM mf_data WHERE city = %s AND date::date = %s
    """
    cur.execute(query_max_rain, (city, date_str))
    max_rain = cur.fetchone()[0]
    
    # Requête pour récupérer la neige
    query_max_snow = """
        SELECT MAX(rain) FROM mf_data WHERE city = %s AND date::date = %s
    """
    cur.execute(query_max_snow, (city, date_str))
    max_snow = cur.fetchone()[0]

    # Requête pour récupérer le taux d'humidité 
    query_max_hum = """
        SELECT MAX(hum) FROM mf_data WHERE city = %s AND date::date = %s
    """
    cur.execute(query_max_hum, (city, date_str))
    max_hum = cur.fetchone()[0]
    
    # Requête pour récupérer la vitesse maximale du vent
    query_max_windspeed = """
        SELECT windspeed FROM mf_data WHERE city = %s AND date::date = %s ORDER BY windspeed DESC LIMIT 1
    """  
    cur.execute(query_max_windspeed, (city, date_str))
    max_windspeed = cur.fetchone()[0]
    print(max_windspeed)
    
    # Requête pour récupérer la direction du vent correspondant à la vitesse maximale
    query_winddir = """
        SELECT winddirection FROM mf_data WHERE city = %s AND date::date = %s AND windspeed = %s
    """
    cur.execute(query_winddir, (city, date_str, max_windspeed))
    winddir = cur.fetchone()[0]
    
    # Requête pour récupérer la description météorologique la plus fréquente
    query_description = """
        SELECT descr FROM mf_data WHERE city = %s AND date::date = %s GROUP BY descr ORDER BY COUNT(*) DESC LIMIT 1
    """
    cur.execute(query_description, (city, date_str))
    description = cur.fetchone()[0]
    
    weather_data = f"pour la ville {city} le {date_str} la température maximale sera de {max_temp}, la température minimale sera de {min_temp}, il pleuvra {max_rain} mm par heure au plus, il neigera {max_snow} mm par heure au plus, le taux d'humidité maximale aujourd'hui est de {max_hum}, il ventera à {max_windspeed} sur l'échelle de Beaufort dans la direction {winddir}, le temps sera essentiellement : {description}"
 
    return weather_data

def delete_data_forecast(cur, conn):
    cur.execute("DELETE FROM mf_data")
    conn.commit()

def delete_old_wf(cur, conn):
    update_dt = format_update_dt()
    print("update_dt:", update_dt)
    update_dt = datetime.strptime(update_dt, '%d-%m-%Y %H:%M:%S') 
    print("update_dt:", update_dt)
    today = update_dt - timedelta(hours=6)
    today_str = today.strftime('%d-%m-%Y %H:%M:%S')
    print("today_str:", today_str)
    cur.execute("DELETE FROM mf_data WHERE to_timestamp(update_dt, 'DD-MM-YYYY HH24:MI:SS') <= %s", (today_str,))
    conn.commit()
    
def close_connection(conn):
    conn.close()
    print("la connexion est fermée")

# Fonction qui va créer une table qui reprend la date, la température minimum, la température maximum, le lever et le coucher du soleil