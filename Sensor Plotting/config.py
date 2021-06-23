# MQTT
broker = "localhost"
port = 1883
QOS = 1

topic_sub_stream = "sensor/+/reading/stream"
topic_publish_reply = "sensor/{}/reading/reply"

publish = True    # Enable MQTT publishing after processing

# Processing
standard_trigger = 37.1
method = "cv2.TM_CCOEFF"
template = 'C:/Program Files/sensor plotting/head.png'
scale = 20        # Amount the image should be scaled

display = False   # Enable cv2.imshow()
batch = 15        # Amount the sensor has to send before processing starts

# Alerts
path = 'C:/Program Files/sensor plotting/alerts'    # .jpg trigger image save path

# Initial
queue = {}        # dictionary used to store sensor names and corresponding frames
reply_list = []   # used to store results while testing
