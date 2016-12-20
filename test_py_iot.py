#!/usr/bin/env python
from devicehub.devicehub import Sensor, Actuator, Device, Project
from random import randint
from time import sleep


PROJECT_ID = '8470'
DEVICE_UUID = 'e894686a-3d26-49bc-bf03-2a3d9cdad4a8'
API_KEY = '38637f26-c6a8-4b57-b3ce-0c63ad990ce8'


def on_switch(data):
    """
    Whenever an actuator receives a command from DeviceHub.net, it's state property is updated.
    The received data is also passed to the callback as a dictionary consisting of 'timestamp' and 'state'.
    timestamp - contains the unix timestamp at which the actuator was commanded
    state - contains the new actuator state
    """
    print('Received command to toggle the switch: ', switch.state)


def on_frontfloodlight(data):
    print('Received command to toggle flood light: ', floodlight.state)


# We want the data to be saved to disk before sending it to DeviceHub.net so we're setting persistent to True
# This also ensures that the project data stored locally is loaded if it exists.
project = Project(PROJECT_ID, persistent=False)

device = Device(project, DEVICE_UUID, API_KEY)

# log = Sensor(Sensor.STRING, 'Log')

floodlight = Actuator(Actuator.DIGITAL, 'frontfloodlight')
switch = Actuator(Actuator.DIGITAL, 'Switch')

# Passing logger=True also sends all log output to this string sensor.
# device.addSensor(log, logger=True)


device.addActuator(floodlight, on_frontfloodlight)
device.addActuator(switch, on_switch)

print("Device initialized successfully")
# log.addValue('Device initialized successfully.')

