import network
from machine import Pin

status = Pin(2, Pin.OUT)  # Blue onboard LED


#
#   Network functions
#

SSID = ""
WPA2 = ""

wlan_if = network.WLAN(network.STA_IF)


def wlan_connect():
    """Handles WLAN connection for the board,
       returns the interface object when a
       connection is active.
    """
    if not wlan_check():
        print('connecting to network...')
        wlan_if.active(True)
        wlan_if.connect(SSID, WPA2)
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
    """Accepts 'color' as red, yellow or green.
       Toggles Pin.out depending on color.
    """
    r = Pin(GPIO, Pin.OUT)
    y = Pin(GPIO, Pin.OUT)
    g = Pin(GPIO, Pin.OUT)

    if color == "red":
        r.value(1)
        y.value(0)
        g.value(0)
    elif color == "yellow":
        r.value(0)
        y.value(1)
        g.value(0)
    elif color == "green":
        r.value(0)
        y.value(0)
        g.value(1)


if __name__ == "__main__":
    wlan_connect()
    print('network config:', wlan_if.ifconfig())
