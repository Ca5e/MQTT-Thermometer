import utime

import machine

import config


def stoplight(color="none"):
    """Accepts 'color' as red, yellow or green
       Other inputs turn off all lights.
       Toggles Pin.out depending on color.
    """
    for x in [config.redPin, config.ylwPin, config.grnPin]:
        machine.Pin(x, machine.Pin.OUT).value(0)

    if color == "red":
        machine.Pin(config.redPin, machine.Pin.OUT).value(1)
    elif color == "yellow":
        machine.Pin(config.ylwPin, machine.Pin.OUT).value(1)
    elif color == "green":
        machine.Pin(config.grnPin, machine.Pin.OUT).value(1)
    return color


def light_test():
    for _ in range(4):
        for x in [config.redPin, config.ylwPin, config.grnPin, config.status]:
            pin = machine.Pin(x, machine.Pin.OUT)
            pin.value(not pin.value())
            utime.sleep(.07)


def display(reading, ambient, duration, trigger, accuracy, result):
    """update screen and lights to display reply.
    """
    # example reply data: 30.312, 19.432, 892, 37.1, 90, 1
    print("Updating screen with: " + reading)

    if result == "0":
        print("\n     Normal measurement\n")
        stoplight("green")
    elif result == "1":
        print("\n     Trigger value exceeded\n")
        stoplight("red")
    elif result == "2":
        print("\n     No face detected\n")
        stoplight("yellow")
    elif result == "3":
        print("\n     Object too close/too far\n")
        stoplight("yellow")


if __name__ == "__main__":
    light_test()
    pass
