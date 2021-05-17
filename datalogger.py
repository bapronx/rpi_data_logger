import yaml
import requests
import time
import random
import datetime
from typing import Tuple
import Aafruit_DHT
with open("config.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


KEY = config["API_KEY"]
REFRESH_TIMER_SEC = config["REFRESH_TIMER_SEC"]
MODEL_NUMBER = config["MODEL_NUMBER"]
GPIO_NUMBER = config["GPIO_NUMBER"]

def push_data(temp:float, humidity:float):
    '''Takes temperature and humidity readings and pushes data to ThingSpeak server'''
    #Set up request url and parameters
    url = 'https://api.thingspeak.com/update'
    params = {'key': KEY, 'field1': humidity, 'field2': temp}
    #Publish values to ThingSpeak
    res = requests.get(url, params=params)

def get_data() -> Tuple[int,int]:
    humidity, temperature = Adafruit_DHT.read_retry(MODEL_NUMBER, GPIO_NUMBER)
    return temperature, humidity

def log_data(temp:float, humidity:float):
        now = datetime.datetime.now()
        with open(config["local_db"], "a") as file:
            file.write(f"{now.timestamp()}, {temp}, {humidity} \n")

if __name__ == "__main__":
    while True:
        data = get_data()
        log_data(*data)
        push_data(*data)
        time.sleep(REFRESH_TIMER_SEC) # Wait 60 seconds