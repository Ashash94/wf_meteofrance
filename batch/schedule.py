import platform
import schedule
import time
from datetime import datetime

from city_list import get_cities_list
from meteo import connect_bdd, fetch_data_table_mf, close_connection, delete_old_wf

def update_wf():
    update_dt_wf = datetime.now()
    cur, conn = connect_bdd()
    cities_list = get_cities_list(cur)
    wf = fetch_data_table_mf(cur, conn, cities_list)
    if wf is not None :
        delete_old_wf(cur, conn)
        print("Les données caduques ont bien été supprimées.")
    close_connection(conn)
    print(f"La mise à jour été le {update_dt_wf}")


schedule.every().day.at("01:10").do(update_wf)
schedule.every().day.at("06:05").do(update_wf)
schedule.every().day.at("12:10").do(update_wf)
schedule.every().day.at("18:05").do(update_wf)

if platform.system() == 'Windows':
    while True:
        schedule.run_pending()
        time.sleep(60)
else:
    while True:
        schedule.run_pending()
        time.sleep(60)
