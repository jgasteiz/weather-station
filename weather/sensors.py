import dataclasses

import smbus

DEVICE_BUS = 1
DEVICE_ADDR = 0x17

TEMP_REG = 0x01
LIGHT_REG_L = 0x02
LIGHT_REG_H = 0x03
STATUS_REG = 0x04
ON_BOARD_TEMP_REG = 0x05
ON_BOARD_HUMIDITY_REG = 0x06
ON_BOARD_SENSOR_ERROR = 0x07
BMP280_TEMP_REG = 0x08
BMP280_PRESSURE_REG_L = 0x09
BMP280_PRESSURE_REG_M = 0x0A
BMP280_PRESSURE_REG_H = 0x0B
BMP280_STATUS = 0x0C
HUMAN_DETECT = 0x0D


@dataclasses.dataclass
class ReadingResults:
    outside_temperature: int
    onboard_temperature: int
    onboard_humidity: int
    barometer_temperature: int
    barometer_pressure: int
    light_sensor: int
    human_detected: bool

    def __str__(self):
        return (
            f"outside_temperature: {self.outside_temperature}\n"
            f"onboard_temperature: {self.onboard_temperature}\n"
            f"onboard_humidity: {self.onboard_humidity}\n"
            f"barometer_temperature: {self.barometer_temperature}\n"
            f"barometer_pressure: {self.barometer_pressure}\n"
            f"light_sensor: {self.light_sensor}\n"
            f"human_detected: {self.human_detected}\n"
        )


def sample_reading() -> ReadingResults:
    bus = smbus.SMBus(DEVICE_BUS)

    reading_results_kwargs = {
        "outside_temperature": None,
        "onboard_temperature": None,
        "onboard_humidity": None,
        "barometer_temperature": None,
        "barometer_pressure": None,
        "light_sensor": None,
        "human_detected": False,
    }

    aReceiveBuf = [0x00]

    for i in range(TEMP_REG, HUMAN_DETECT + 1):
        aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

    if aReceiveBuf[STATUS_REG] & 0x01:
        print("Off-chip temperature sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x02:
        print("No external temperature sensor!")
    else:
        reading_results_kwargs["outside_temperature"] = aReceiveBuf[TEMP_REG]

    if aReceiveBuf[STATUS_REG] & 0x04:
        print("Onboard brightness sensor overrange!")
    elif aReceiveBuf[STATUS_REG] & 0x08:
        print("Onboard brightness sensor failure!")
    else:
        light_sensor_value = aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]
        reading_results_kwargs["light_sensor"] = light_sensor_value

    reading_results_kwargs["onboard_temperature"] = aReceiveBuf[ON_BOARD_TEMP_REG]
    reading_results_kwargs["onboard_humidity"] = aReceiveBuf[ON_BOARD_HUMIDITY_REG]

    if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0:
        print("Onboard temperature and humidity sensor data may not be up to date!")

    if aReceiveBuf[BMP280_STATUS] == 0:
        barometer_temperature = aReceiveBuf[BMP280_TEMP_REG]
        barometer_pressure = (
            aReceiveBuf[BMP280_PRESSURE_REG_L]
            | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8
            | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16
        )
        reading_results_kwargs["barometer_temperature"] = barometer_temperature
        reading_results_kwargs["barometer_pressure"] = barometer_pressure
    else:
        print("Onboard barometer works abnormally!")

    human_detected = aReceiveBuf[HUMAN_DETECT] == 1
    reading_results_kwargs["human_detected"] = human_detected

    return ReadingResults(**reading_results_kwargs)
