import network
from machine import Pin

led = Pin(2, Pin.OUT)  # Blue onboard LED


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
        led.value(1)
        return True
    else:
        led.value(0)
        return False


if __name__ == "__main__":
    wlan_connect()
    print('network config:', wlan_if.ifconfig())
