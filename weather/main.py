import time

from . import sensors


def start_weather_station():
    print("Starting the weather station")
    while True:
        sensors.sample_reading()
        time.sleep(5)
