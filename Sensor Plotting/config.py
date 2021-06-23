# MQTT
broker = "localhost"
port = 443
QOS = 1

topic_sub_stream = "sensor/+/reading/stream"
topic_publish_reply = "sensor/{}/reading/reply"

# Processing
standard_trigger = 37.1
template = 'C:/Program Files/sensor plotting/head.png'
scale = 20 # Amount the image should be scaled
method = "cv2.TM_CCOEFF"

display = False
batch = 15
publish = True

# Alerts
path = 'C:/Program Files/sensor plotting/alerts'

# Initial
queue = {}
reply_list = []
