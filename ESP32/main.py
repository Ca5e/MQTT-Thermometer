import time
import random
from boot import wlan_connect, wlan_check, stoplight

serverUrl = "http://example.com/post-esp-data.php"
keyAPI = "rNum"

sensorName = "ESP32/2"
sensorLocation = "GPS data"

device_on = True


def temp_sensor():
    """Random reading returned as float.
    """
    time.sleep(2)
    return random.uniform(32, 38)


def scan():
    """Scanning logic
    """
    scanning = True
    trigger = 37.1
    while scanning:
        stoplight("yellow")
        if temp_sensor() > trigger:
            stoplight("red")
        elif temp_sensor() < trigger:
            stoplight("green")


def loop():
    """Continues loop
    """
    count = 0
    while device_on:
        count += 1
        if count % 10:
            if not wlan_check():
                wlan_connect()
        scan()


if __name__ == "__main__":
    loop()
