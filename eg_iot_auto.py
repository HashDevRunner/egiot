import paho.mqtt.client as mqtt
from datetime import datetime as dt
from datetime import timedelta as delta
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
GPIO.setwarnings(False)

#-------------------------------------------
# Adjust times here
#-------------------------------------------
TIME_ON = "18:00"
TIME_OFF = "05:30"

time_off = time.strptime(TIME_OFF,"%H:%M")
time_on = time.strptime(TIME_ON,"%H:%M")
time_mid = time.strptime("00:00","%H:%M")

#determine ON and OFF times
dt_now = dt.now()

#Uncomment for testing
#TIME_NOW_TEST = "05:31"
#time_now_test = time.strptime(TIME_NOW_TEST,"%H:%M")
#dt_now = dt.now().replace(hour=time_now_test.tm_hour, minute=time_now_test.tm_min) + delta(days = 1)

dt_time_on = dt_now.replace(hour=time_on.tm_hour, minute=time_on.tm_min)
if(dt_now >= dt_time_on):
  dt_time_off = (dt_now + delta(days = 1)).replace(hour=time_off.tm_hour, minute=time_off.tm_min)
else:
  dt_time_off = dt_now.replace(hour=time_off.tm_hour, minute=time_off.tm_min)

print("Time now: " + dt_now.strftime("%m/%d %H:%M"))
print("Time on: " + dt_time_on.strftime("%m/%d %H:%M"))
print("Time off: " + dt_time_off.strftime("%m/%d %H:%M"))

#initialize mqtt
client = mqtt.Client()
try:
  client.connect("test.mosquitto.org", 1883, 60)
except:
  client.connect("broker.hivemq.com", 1883, 60)

def turn_on():
  GPIO.output(GARAGELIGHT_PIN, ON)
  client.publish(LOG_TOPIC, dt_now.strftime("%m/%d %H:%M") + '- status:ON')

def turn_off():
  GPIO.output(GARAGELIGHT_PIN, OFF)
  client.publish(LOG_TOPIC, dt_now.strftime("%m/%d %H:%M") + '- status:OFF')

#-------------------------------------------
# MAIN LOGIC HERE!!! 
# turn on from 6pm to 5:30am
#-------------------------------------------
if(dt_now >= dt_time_on or dt_now < dt_time_off):
  print("Turning ON...")
  turn_on()

elif( dt_now >= dt_time_off):
  print("Turning OFF...")
  turn_off()

else:
  print("why i'm on else???")

client.disconnect()

