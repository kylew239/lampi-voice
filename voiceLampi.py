import subprocess
import json
import os
import time
import signal
import speech_recognition as sr
import paho.mqtt.client as MQTT
from lamp_common import *
import sys
from time import sleep
from paho.mqtt.client import Client

MIC_INDEX = 2
MQTT_CLIENT_ID = "voice"

class LampiVoice(object):
    def __init__(self):
        self.received_lamp_state = {}
        self.client = Client(client_id=MQTT_CLIENT_ID)
        self.client.enable_logger()
        self.client.on_connect = self.on_connect
        self.client.connect(MQTT_BROKER_HOST,
                            port=MQTT_BROKER_PORT,
                            keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        self._wait_for_lamp_state()
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.message_callback_add(TOPIC_LAMP_CHANGE_NOTIFICATION,
                                    self._receive_lamp_state)
        client.subscribe(TOPIC_LAMP_CHANGE_NOTIFICATION, qos=1)

    def _receive_lamp_state(self, client, userdata, message):
        self.received_lamp_state = json.loads(message.payload.decode('utf-8'))

    def _wait_for_lamp_state(self):
        for _ in range(10):
            if self.received_lamp_state:
                return
            self.client.loop(timeout=0.05)
        raise Exception("Timeout waiting for lamp state")

    def return_lamp_state(self):
        print("here")
        return self.received_lamp_state
        

def parseText(text):
    voice = LampiVoice()
    lampState = voice.return_lamp_state()

    if "lamp" in text:
        c = MQTT.Client(client_id=MQTT_CLIENT_ID)
        c.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
                keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        c.loop_start()

        if "on" in text:
            print("ON IS FOUND")
            lampState['on'] = True

        if "off" in text:
            print("OFF IS FOUND")
            lampState['on'] = False

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
        parseText(query.split())
    except:
        query = "failed"
    print(query)




while True:
    recordCommand()
