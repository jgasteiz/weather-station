import time

from . import sensors


def start_weather_station():
    print("Starting the weather station")
    while True:
        results = sensors.sample_reading()
        print(results, flush=True)
        time.sleep(1)
