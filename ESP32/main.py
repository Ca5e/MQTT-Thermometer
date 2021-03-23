from boot import wlan_connect, wlan_check

serverUrl = ""
keyAPI = ""

sensorName = "ESP32/2"
sensorLocation = "GPS data"

device_on = True


def loop():
    count = 0
    while device_on:
        count += 1
        if count % 10:
            if not wlan_check():
                wlan_connect()


if __name__ == "__main__":
    loop()
