import uasyncio as asyncio

import config
import simulation
from mqtt.mqtt_as import MQTTClient
from boot import stoplight, display

if config.ftp:
    import ftp.uftpd
import utime as time


def callback(topic, msg, retained):
    """Coroutine, executed if a message is received.
    """
    topic = topic.decode('ascii')
    msg = msg.decode('ascii')

    print("MQTT " + topic + ": " + msg)

    if topic == config.topic_sub_mode:
        msg = msg.lower()
        if msg != config.mode and msg in ["standby", "scan", "monitor"]:
            config.mode = msg
            print("Mode updated to: " + msg)
    elif topic == config.topic_sub_reply:
        # example data: 30.312;19.432;892;37.1;90;1;
        msg = msg.split(";")
        display(msg[0], msg[1], msg[2], msg[3], msg[4], msg[5])


async def publish_status(online="True"):
    """Publishes current status (of system config).
    """
    global client
    await client.publish(config.topic_pub_online, online, retain=True, qos=0)
    await client.publish(config.topic_pub_geo, '{}'.format(config.location), retain=True, qos=0)
    print("Publishing online as " + online + " and updating location")


async def conn_han(client):
    """Coroutine, executed once broker connection is active.
    """
    await client.subscribe(config.topic_sub_reply, 1)
    await client.subscribe(config.topic_sub_mode, 1)

    await asyncio.create_task(publish_status())


async def main(client):
    try:
        sensor = simulation.Sensor()
        loop = asyncio.get_event_loop()
        loop.create_task(sensor.start())
        await client.connect()
        while True:
            try:
                while config.mode == "standby":
                    # standby mode: the sensor waits until the
                    # mode is changed.
                    stoplight("red")
                    await sensor.stop()
                    await asyncio.sleep(2)
                while config.mode == "scan":
                    if not sensor.running:
                        loop.create_task(sensor.start())

                    # scan mode: the sensor only sends data when
                    # movement is detected.
                    reading = sensor.read()

                    if len(reading) > 0:
                        print(reading[0][0])

                    await asyncio.sleep(1 / config.fps)
                while config.mode == "monitor":
                    if not sensor.running:
                        loop.create_task(sensor.start())

                    # monitor mode: the sensor sends all sensor data,
                    # even if no movement is detected.

                    start = time.ticks_ms()
                    await client.publish(config.topic_pub_reading, '{}'.format(sensor.read()), qos=0)
                    end = time.ticks_ms()
                    print("Published sensordata, time taken: " + str(time.ticks_diff(end, start)) + "ms")

                    await asyncio.sleep(1 / config.fps)
            except Exception as e:
                print("Error in main(client): " + str(e))
                await asyncio.sleep(2)
    finally:
        # offline mode: the sensor changes the status
        # to 'offline' when it turns off.
        await asyncio.create_task(publish_status(online="False"))


if __name__ == "__main__":
    config.connection['subs_cb'] = callback
    config.connection['connect_coro'] = conn_han
    # last will message: broker sends (online 'false') after unexpected disconnect.
    config.connection['will'] = [config.topic_pub_online, "False", True, 1]

    MQTTClient.DEBUG = True  # Print diagnostic messages
    client = MQTTClient(config.connection)
    try:
        asyncio.run(main(client))
    finally:
        client.close()
