import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

TOPIC_1 = 'e5dfe1bd76'
FLOODLIGHT_PIN = 23

TOPIC_2 = 'e5dfe1bd77'
GARAGELIGHT_PIN = 24 
GPIO.setmode(GPIO.BCM)
ON = 0
OFF = 1

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
                    (TOPIC_2,0)])

def on_message(client,userdata, msg):
  print "Topic:", msg.topic + '\nMessage:' + str(msg.payload)
  if( msg.topic == TOPIC_1 ):
    send_command(FLOODLIGHT_PIN, str(msg.payload))
  elif( msg.topic == TOPIC_2 ):
    send_command(GARAGELIGHT_PIN, str(msg.payload))
  else:
    print("Unknown Topic...")
   

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()

