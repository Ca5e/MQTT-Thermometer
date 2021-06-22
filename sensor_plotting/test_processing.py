import unittest
import processing
import config
import simulation

from mqtt import get_mqtt_client


class SensorTestCase(unittest.TestCase):
    """Tests for processing.py"""
    
    def setUp(self):
        self.sensor = "test-sensor"
        self.frames = simulation.data[60:80]
        self.batch = 20

        self.display = True     # Toggle opencv window
        self.publish = True     # Toggle MQTT publish

        # If self.publish == True, start mqtt connection.
        if self.publish:
            self.client = get_mqtt_client()
            self.client.connect(config.broker, port=config.port)
        else:
            self.client = None

        # add all the selected frames to the queue:
        for msg in self.frames:
            config.queue.setdefault(self.sensor, []).append(msg)

    def test_full_script(self):
        processing.start(self.sensor, self.client, self.display, self.batch, self.publish)

        # run assert for every single reply
        for result in config.reply_list:
            # Expecting results similar to: "31.389;23.939;507;37.1;88;0;"
            # Format: reading;ambient;duration;trigger;accuracy;result;
            result = result.split(";")

            # reading result must be between 1 degrees of original
            if result[0] != "None":
                self.assertAlmostEqual(float(result[0]), 31.5, delta=1)

unittest.main()
