import json

from meteo import data_new_city_mf

list_domtom = ['971', '972', '973', '974', '975', '976', '978', '984', '986', '987', '988', '989']

# Ouvrir le fichier .json qui permet de créer la liste et la table de villes
def open_cities_json():
    with open('data/cities.json', 'r') as file:
        city_file = json.load(file)
        return city_file
        
# Création de la table
def create_table_cities(cur, conn):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cities_mf (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            postCode VARCHAR(5),
            department VARCHAR(3),
            region VARCHAR(70),
            latitude FLOAT,
            longitude FLOAT
        )
        """
    )
    conn.commit()
    print("La table a bien été créée ou existe déjà.")

def fill_table_cities(cur, conn, city_file):
    cur.execute("SELECT city FROM cities_mf")
    rows = cur.fetchone()
    if rows is None:
        #Insérer les données de ville dans la table
        for city in city_file['cities']:
            if city['department_number'] not in list_domtom:   
                cur.execute(
                    """
                    INSERT INTO cities_mf (city, postcode, department, region, latitude, longitude) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (city['label'], city['zip_code'], city['department_number'], city['region_name'], city['latitude'], city['longitude'])
                )
                conn.commit()
                print(f"Ajout dans la table : La ville {city['label']} a été insérée avec succès.")
                
            else:
                print(f"Ajout dans la table : Non car la ville {city['label']} se situe hors France Métropolitaine")
    else :
        print("La table cities contient déjà des données. Aucune action nécessaire.")

def get_cities_list(cur):     
    cur.execute("SELECT city, postcode FROM cities_mf")

    cities = cur.fetchall()
    
    cities_list = [] #liste vide
    
    for row in cities:
        cities_list.append({'city': row[0], 'postcode': row[1]})
    return cities_list


# Fonction qui vérifie l'existance d'une ville dans la base de données

def check_expected_city_in_db(city, cur, conn):
    try:
        cur.execute(
            """
            SELECT EXISTS(SELECT 1 FROM cities_mf WHERE city = %s)
            """,
            (city,)
        )
        
        exists = cur.fetchone()[0]
        
        if not exists:
            with open('data/cities_full.json', 'r') as file:
                data = json.load(file)
                
            for c in data['cities']:
                if c['label'] == city:
                    if c["department_number"] not in list_domtom:
                        cur.execute(
                            """
                            INSERT INTO cities_mf (city, postcode, department, region, latitude, longitude) 
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (c['label'], c['zip_code'], c['department_number'], c['region_name'], c['latitude'], c['longitude'])
                        )
                        conn.commit()
                        print(f"La ville {c['label']} a été insérée avec succès.")
                        
                        city = c['label']
                        postcode = c['zip_code']                                  
                        data_new_city_mf(cur, conn, city, postcode)  
                    else:
                        print(f"La ville {c['label']} se situe hors France Métropolitaine")
                    break
            else:
                print("La ville renseignée n'existe pas dans le référentiel des villes de data.gouv")

        else:
            print(f"La ville {city} existe déjà dans la table.")
            
    except Exception as e:
        print("Une erreur s'est produite:", e)

def delete_data_cities(cur, conn):
    cur.execute("DELETE FROM cities_mf")
    conn.commit()
    print("Les données ont bien été supprimées.")
