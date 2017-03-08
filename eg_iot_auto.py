import paho.mqtt.client as mqtt
from datetime import datetime as dt
import RPi.GPIO as GPIO
import time

TOPIC_1 = 'e5dfe1bd76'
FLOODLIGHT_PIN = 23
FLOODLIGHT_STATUS = 0 

TOPIC_2 = 'e5dfe1bd77'
GARAGELIGHT_PIN = 24 
GARAGELIGHT_STATUS = 0
GPIO.setmode(GPIO.BCM)
ON = 0
OFF = 1

LOG_TOPIC = 'e5dfe1bd77/log'
STATUS_TOPIC = 'e5dfe1bd77/status'

GPIO.setup(FLOODLIGHT_PIN, GPIO.OUT)
GPIO.setup(GARAGELIGHT_PIN, GPIO.OUT) 
#GPIO.output(FLOODLIGHT_PIN, OFF)
#GPIO.output(GARAGELIGHT_PIN, OFF)

GPIO.setwarnings(False)

time_off = time.strptime("06:00","%H:%M")
time_on = time.strptime("18:00","%H:%M")
time_mid = time.strptime("00:00","%H:%M")

now = dt.now().strftime("%H:%M")
time_now = time.strptime(now,"%H:%M")

#initialize mqtt
client = mqtt.Client()
try:
  client.connect("test.mosquitto.org", 1883, 60)
except:
  client.connect("broker.hivemq.com", 1883, 60)

#execute PIN requests
print("Raspberry time auto: " + now)
#turn on from 6PM to 6AM
if (time_now > time_on) or (time_now > time_mid and time_now < time_off): 
  print("Turning ON...")
  GPIO.output(GARAGELIGHT_PIN, ON)
  client.publish(LOG_TOPIC,'PI: ' + now+ '- status:ON')

elif time_now > time_off :
#turn off from 6AM to 6PM
  print("Turning OFF...")
  GPIO.output(GARAGELIGHT_PIN, OFF)
  client.publish(LOG_TOPIC,'PI: ' + now + '- status:OFF')

client.disconnect()

