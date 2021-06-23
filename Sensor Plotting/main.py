"""
Subscribes to the stream topic and starts processing thread.
"""
import time
import threading
import datetime

from mqtt import get_mqtt_client

import processing
import config

def on_message(client, userdata, msg):
    """Funtion that gets executed when a publish message is received.
    """
    now = datetime.datetime.now()
    sensor = msg.topic.split('/')[1]
    print(f"Stream data from {sensor} at {now}")

    config.queue.setdefault(sensor, []).append(msg)
    try:
        # start thread with name 'sensor' if it doesn't exist yet:
        if sensor not in str(threading.enumerate()):
            threading.Thread(target=processing.start, args=(sensor, client), name=sensor).start()
    except Exception as e:
        print("on_message(): " + str(e))


def main():
    print("script starting")
    client = get_mqtt_client()
    client.on_message = on_message
    client.connect(config.broker, port=config.port)
    print("connecting...")
    client.subscribe(config.topic_sub_stream)
    time.sleep(4)  # Wait for connection setup to complete
    client.loop_forever()


if __name__ == "__main__":
    main()
