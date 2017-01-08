import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

TOPIC_1 = 'Floodlight1'
FLOODLIGHT_PIN = 02

TOPIC_2 = 'Garagelight'
GARAGELIGHT_PIN = 03 
GPIO.setmode(GPIO.BCM)

GPIO.setup(FLOODLIGHT_PIN, GPIO.OUT)
GPIO.setup(GARAGELIGHT_PIN, GPIO.OUT) 

print("Raspberry IoT initialized...")

#--------------------------------------------------------------------------
#---------------- This section is for floodlight pin ----------------------
#--------------------------------------------------------------------------

def send_command(pin, msg):
  print "Sending PIN#" + str(pin) + " command: " + msg
  if( msg == '1'):
    GPIO.output(pin, 1)
  else:
    GPIO.output(pin, 0)

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

client.connect("localhost", 1883, 60)

client.loop_forever()

