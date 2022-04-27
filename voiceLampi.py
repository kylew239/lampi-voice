import subprocess
import json
import os
import time
import signal
import speech_recognition as sr
import paho.mqtt.client as MQTT
from lamp_common import *
from settings import *

MIC_INDEX = 2
MQTT_CLIENT_ID = "voice"
lampState = {}


def receive_new_lamp_state(self, client, userdata, message):
    lampState = json.loads(message.payload.decode('utf-8'))
    print("NEW LAMP STATE")
    print(lampState)
    return lampState


def get_current_lamp_state():
    c = MQTT.Client(client_id=MQTT_CLIENT_ID)
    c.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
              keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
    c.subscribe(TOPIC_LAMP_CHANGE_NOTIFICATION, qos=1)
    c.message_callback_add(TOPIC_LAMP_CHANGE_NOTIFICATION,
                           receive_new_lamp_state)


def parseText(text):
    print("getting current state")
    # lampState = get_current_lamp_state()
    c = MQTT.Client(client_id=MQTT_CLIENT_ID)
    c.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
              keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
    c.loop_start()
    print(lampState)

    if "on" in text:
        print("ON IS FOUND")
        lampState['on'] = True

    if "off" in text:
        print("OFF IS FOUND")
        lampState['on'] = False

    if "red" in text:
        lampState['color'] = {'h': 1.0, 's': 1.0}
        lampState['on'] = True

    if "blue" in text:
        lampState['color'] = {'h': 0.6, 's': 1.0}
        lampState['on'] = True

    if "green" in text:
        lampState['color'] = {'h': 0.35, 's': 1.0}
        lampState['on'] = True

    if "yellow" in text:
        lampState['color'] = {'h': 0.2, 's': 1.0}
        lampState['on'] = True

    if "dim" in text:
        lampState['brightness'] = .25
        lampState['on'] = True

    if "brighten" in text:
        lampState['brightness'] = 1.0
        lampState['on'] = True

#   if "hue" in text:
#       print("HUE IS FOUND")
#       lampState['color']['h'] =

    lampState['client'] = MQTT_CLIENT_ID
    print(lampState)
    c.publish(TOPIC_SET_LAMP_CONFIG,
              json.dumps(lampState).encode('utf-8'),
              qos=1)
    print("published")
    c.loop_stop()


def recordCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=MIC_INDEX) as source:
        r.adjust_for_ambient_noise(source)
        print("listening...")
        r.pause_threshold = .5
        audio = r.listen(source)

    try:
        print("recognizing...")
        query = r.recognize_google(audio)

        # setting language makes it slower but more accurate
        # query = r.recognize_google(audio, language = 'en-US')
        parseText(query)
    except:
        query = "failed"
    print(query)


while True:
    recordCommand()
