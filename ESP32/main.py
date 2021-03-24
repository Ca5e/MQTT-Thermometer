import time
import random
import config
import machine
from boot import wlan_connect, wlan_check, stoplight


def temp_sensor():
    """Random reading returned as float.
    """
    time.sleep(2)
    return random.uniform(30, 40)


def scan():
    """Scanning logic
    """
    scanning = True
    while scanning:
        stoplight("yellow")
        print("Scanning...")

        reading = temp_sensor()
        if reading > config.trigger:
            print("Trigger value exceeded, red light")
            stoplight("red")
        elif reading < config.trigger:
            print("Scan successful, green light")
            stoplight("green")

        time.sleep(2)       # sleeping so output can be viewed.
        scanning = False


def loop():
    """Continues loop
    """
    count = 0
    while True:
        count += 1
        if count % 10:
            if not wlan_check():
                wlan_connect()
        if config.device_on:
            scan()
        else:
            stoplight("red")
            # if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            #     print("Woke from a deep sleep...")
            # machine.deepsleep(10000)


if __name__ == "__main__":
    loop()
