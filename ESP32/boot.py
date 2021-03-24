import network
import config
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


def stoplight(color):
    """Accepts 'color' as red, yellow or green
       Other inputs turn off all lights.
       Toggles Pin.out depending on color.
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


if __name__ == "__main__":
    wlan_connect()
    print('network config:', wlan_if.ifconfig())
