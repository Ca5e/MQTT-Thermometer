# config.py

# Network configuration:
SSID = "ESP-WiFi"
WPA2 = "Johma Password"

# Device information
sensorName = "ESP32-6"
sensorLocation = "GPS-data"

# Database connection
serverUrl = "http://example.com/post-esp-data.php"
jsonUrl = "http://example.com/config.json"
keyAPI = "rNum87546392"


# Specifics
standby = True
trigger = 37.1

# Stoplight GPIO pins
redPin = 25
ylwPin = 26
grnPin = 27
# Meaning red light is connected to '25', etc.
