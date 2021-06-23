import uasyncio as asyncio
import ujson
import urandom
import machine

import config


class Sensor:
    """Simulates the behaviour of a temperature sensor,
       using txt files with 'large' amounts of data.
    """

    def __init__(self, file="sensor/normal.scan", fps=config.fps, width=32, height=24, random=True):
        self.file = file
        self.fps = fps
        self.random = random

        self.width = width
        self.height = height

        self.running = False
        self.frame = []

    def read(self):
        return self.frame

    async def start(self):
        print("Starting sensor " + config.client_id)
        await asyncio.sleep(4)
        self.running = True

        while self.running:
            try:
                if self.random:
                    await self.randomize_file()
                await asyncio.create_task(self.simulate())
            except Exception as e:
                print("Sensor error: " + str(e))
                await asyncio.sleep(5)

    def stop(self):
        print("Halting sensor")
        self.running = False

    async def randomize_file(self):
        """Add some randomness to the simulation by
           using multiple files.
        """
        rand = urandom.randint(0, 100)
        # simulation 'trigger' is used if boot button is pressed:
        if machine.Pin(0).value() == 0:
            print("\n     Trigger button pressed\n")
            self.file = "sensor/trigger.scan"
        elif rand < 50:
            self.file = "sensor/normal.scan"
        else:
            self.file = "sensor/ambient.scan"

    async def simulate(self):
        """The entire file can't be read into memory
           therefore the data is read 'line by line'.
        """
        try:
            with open(self.file) as data:
                print("Using " + self.file + " as sensordata")
                length = self.width * self.height
                for line in data:
                    # stop the current simulation if the boot button is pressed:
                    if machine.Pin(0).value() == 0 and self.file[7] not in "trigger":
                        return
                    try:
                        if len(line) >= length:
                            self.frame = ujson.loads(line)
                            await asyncio.sleep(1 / self.fps)
                    except Exception as e:
                        print("Simulation error: " + str(e))
        finally:
            data.close()
