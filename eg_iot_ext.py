import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import os

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
GPIO.output(FLOODLIGHT_PIN, OFF)
GPIO.output(GARAGELIGHT_PIN, OFF)

print("Raspberry IoT initialized...")

#--------------------------------------------------------------------------
#---------------- This section is for floodlight pin ----------------------
#--------------------------------------------------------------------------

def send_command(pin, msg):
  print "Sending PIN#" + str(pin) + " command: " + msg
  if( msg == '1'):
    GPIO.output(pin, ON)
  else:
    GPIO.output(pin, OFF)

def on_disconnect(client, userdata, rc):
  print "Client disconnected..."

def on_connect(client, userdata, rc):
  print("Connected with result code:" + str(rc))
  client.subscribe([(TOPIC_1,0),
                    (TOPIC_2,0),
		    (STATUS_TOPIC,0)])
def send_log(msg):
  client.publish(LOG_TOPIC,msg)

def publish_status(msg):
  client.publish(STATUS_TOPIC,msg)

def on_message(client,userdata, msg):
  print "Topic:", msg.topic + '\nMessage:' + str(msg.payload)
  if( msg.topic == TOPIC_1 ):
    send_command(FLOODLIGHT_PIN, str(msg.payload))
    FLOODLIGHT_STATUS = msg.payload
    send_log('Floodlight: ' + msg.payload)
  elif( msg.topic == TOPIC_2 ):
    send_command(GARAGELIGHT_PIN, str(msg.payload))
    GARAGELIGHT_STATUS = msg.payload
    #send_log('Garage: ' + msg.payload)
    send_log('Garage: ' + GARAGELIGHT_STATUS )
  elif( msg.topic == STATUS_TOPIC and msg.payload == 'Check'):
    response = os.system("ping -c 1 " + "172.17.0.1")
    if( response == 0 ):
      publish_status("Network OK")
    else:
      #i wouldn't be receiving this
      publish_status("Network DOWN!")
  else:
    print("Unknown Topic...")
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
  client.connect("test.mosquitto.org", 1883, 60)
except:
  print("trying alternative")
  client.connect("broker.hivemq.com", 1883, 60)

client.loop_forever()

