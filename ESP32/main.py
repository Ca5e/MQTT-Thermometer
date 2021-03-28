import time
import random
import config
import urequests
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
    while True:
        led = stoplight("yellow")
        print("Scanning...")

        reading = temp_sensor()
        if reading > config.trigger:
            print("Trigger value exceeded, red light")
            led = stoplight("red")
        elif reading < config.trigger:
            print("Scan successful, green light")
            led = stoplight("green")

        time.sleep(2)  # sleeping so light output can be viewed.
        return "api_key={}&sensor={}&location={}&value1={}&value2={}&value3={}" \
            .format(config.keyAPI, config.sensorName, config.sensorLocation, config.trigger, reading, led)


def loop():
    """Continues loop
    """
    while True:
        if config.device_on:
            if not wlan_check():
                wlan_connect()
            else:
                httpsRequestData = scan()
                post = urequests.post(config.serverUrl,
                                      data=httpsRequestData,
                                      headers={"content-Type": "application/x-www-form-urlencoded"})
                print(httpsRequestData)
        else:
            stoplight("red")
            # if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            #     print("Woke from a deep sleep...")
            # machine.deepsleep(10000)


if __name__ == "__main__":
    loop()
