import config
import esp32
import time
import random
import urequests
from boot import wlan_connect, wlan_check, stoplight, update_config


def temp_sensor():
    """Random readings returned as floats.
    """
    time.sleep(2)
    sensor = random.uniform(30, 40)
    ambient = (esp32.raw_temperature()-32)*.5556
    distance = random.uniform(1.5, 4)
    return sensor, ambient, distance


def scan():
    """Scanning logic
    """
    while True:
        led = stoplight("yellow")
        print("Scanning...")

        sensor, ambient, distance = temp_sensor()
        if sensor > config.trigger:
            print("Trigger value exceeded, red light")
            led = stoplight("red")
        elif sensor < config.trigger:
            print("Scan successful, green light")
            led = stoplight("green")

        time.sleep(2)  # sleeping so light output can be viewed.
        return "api_key={}&name={}&location={}&ambient={}&distance={}&trigger={}&reading={}&result={}" \
            .format(config.keyAPI, config.sensorName, config.sensorLocation, ambient, distance,
                    config.trigger, sensor, led)


def loop():
    """Continues loop
    """
    while True:
        if not wlan_check():
            wlan_connect()
            continue
        update_config()
        if config.standby:
            stoplight("red")
            time.sleep(3)
            continue

        httpsRequestData = scan()
        # urequests.post(config.serverUrl, data=httpsRequestData,
        # headers={"content-Type": "application/x-www-form-urlencoded"})
        print(httpsRequestData)


if __name__ == "__main__":
    loop()
