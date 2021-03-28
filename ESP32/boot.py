import config
import network
import urequests
from machine import Pin

status = Pin(2, Pin.OUT)  # Blue onboard LED
wlan_if = network.WLAN(network.STA_IF)


def wlan_connect():
    """Handles WLAN connection for the board,
       returns the interface object when a
       connection is active.
    """
    if not wlan_check():
        print('connecting to network...')
        wlan_if.active(True)
        wlan_if.connect(config.SSID, config.WPA2)
        while not wlan_check():
            pass
    wlan_check()
    return wlan_if


def wlan_check():
    """"Returns True if wlan is connected,
        False otherwise. Turns on 'led' when
        connection is active.
    """
    if wlan_if.isconnected():
        status.value(1)
        return True
    else:
        status.value(0)
        return False


def update_config():
    json = urequests.get(config.jsonUrl)
    # update standby value in config.py
    if json.json()[config.sensorName]["standby"] != config.standby:
        config.standby = not config.standby
        print("Standby value was changed to:", config.standby)


def stoplight(color="none"):
    """Accepts 'color' as red, yellow or green
       Other inputs turn off all lights.
       -Toggles Pin.out depending on color.-
    """
    r = Pin(config.redPin, Pin.OUT)
    y = Pin(config.ylwPin, Pin.OUT)
    g = Pin(config.grnPin, Pin.OUT)
    r.value(0)
    y.value(0)
    g.value(0)

    if color == "red":
        r.value(1)
    elif color == "yellow":
        y.value(1)
    elif color == "green":
        g.value(1)
    return color


if __name__ == "__main__":
    wlan_connect()
    update_config()
    print('network config:', wlan_if.ifconfig())
