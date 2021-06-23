# config.py
from mqtt.mqtt_as import config as connection

# Wi-Fi connection
connection["ssid"] = "SSID"
connection["wifi_pw"] = "password"

# Activate a small FTP server,
# to make file transfer easier.
ftp = False


# MQTT connection
connection["server"] = "server ip/domain"
connection["port"] = 1883

client_id = connection["client_id"].decode("ascii")

topic_pub_reading = "sensor/%s/reading/stream" % client_id
topic_sub_reply = "sensor/%s/reading/reply" % client_id

topic_pub_geo = "sensor/%s/status/geo" % client_id
topic_pub_online = "sensor/%s/status/online" % client_id
topic_sub_mode = "sensor/%s/update/mode" % client_id


# Specifics
mode = "monitor"       # default mode
trigger = 37.1
fps = 2

longitude = 53.004957
latitude = 6.924788

location = str(longitude) + ";" + str(latitude) + ";"


# GPIO pins
redPin = 25     # Meaning red light is connected to '25', etc.
ylwPin = 26
grnPin = 27
# Onboard status light
status = 2
