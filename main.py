import os
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))
weather_dir = os.path.join(project_dir, "weather")
sys.path.insert(0, weather_dir)

if __name__ == "__main__":
    import weather

    weather.start_weather_station()
