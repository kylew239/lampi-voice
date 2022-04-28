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
import csv
import random
#from word2number import w2n

MIC_INDEX = 2
MQTT_CLIENT_ID = "voice"
INTERVAL = .1


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
        return self.received_lamp_state


def parseText(text):
    voice = LampiVoice()
    lampState = voice.return_lamp_state()

    if "lamp" in text:
        c = MQTT.Client(client_id=MQTT_CLIENT_ID)
        c.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
                  keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        c.loop_start()

        lampIndex = text.index("lamp")
        print(lampIndex)
        print(text)
        print(len(text))

        if lampIndex != (len(text) - 1):
            with open('commands.txt') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if row[0] in text:
                        lampState['color'] = {'h': float(row[1]), 's': float(row[2])}
                        lampState['on'] = True

            if "hue" in text:
                hueIndex = text.index("hue")
                if hueIndex != (len(text) -1):
                    if text[hueIndex + 1] == "up" or text[hueIndex + 1] == "increase":
                        lampState['color']['h'] = hsvInc(lampState['color']['h'])
                    if text[hueIndex + 1] == "down" or text[hueIndex + 1] == "decrease":
                        lampState['color']['h'] = hsvDec(lampState['color']['h'])
                    if text[hueIndex + 1].isdigit():
                        lampState['color']['h'] = float(text[hueIndex + 1])/100
                    if text[hueIndex + 1] == "max":
                        lampState['color']['h'] = 1.0
                    if text[hueIndex + 1] == "min":
                        lampState['color']['h'] = 0.0
                    if text[hueIndex + 1] == "random":
                        lampState['color']['h'] = float(random.uniform(0,1))

            if "saturation" in text:
                satIndex = text.index("saturation")
                if satIndex != (len(text) -1):
                    if text[satIndex + 1] == "up" or text[satIndex + 1] == "increase":
                        lampState['color']['s'] = hsvInc(lampState['color']['s'])
                    if text[satIndex + 1] == "down" or text[satIndex + 1] == "decrease":
                        lampState['color']['s'] = hsvDec(lampState['color']['s'])
                    if text[satIndex + 1].isdigit():
                        lampState['color']['s'] = float(text[satIndex + 1])/100
                    if text[satIndex + 1] == "max":
                        lampState['color']['s'] = 1.0
                    if text[satIndex + 1] == "random":
                        lampState['color']['s'] = 0.0
                    if text[satIndex + 1] == "random":
                        lampState['color']['s'] = float(random.uniform(0,1))

            if "brightness" in text:
                brIndex = text.index("brightness")
                if brIndex != (len(text) -1):
                    if text[brIndex + 1] == "up" or text[brIndex + 1] == "increase":
                        lampState['brightness'] = hsvInc(lampState['brightness'])
                    if text[brIndex + 1] == "down" or text[brIndex + 1] == "decrease":
                        lampState['brightness'] = hsvDec(lampState['brightness'])
                    if text[brIndex + 1].isdigit():
                        lampState['brightness'] = float(text[brIndex + 1])/100
                    if text[brIndex + 1] == "max":
                        lampState['brightness'] = 1.0
                    if text[brIndex + 1] == "min":
                        lampState['brightness'] = 0.0
                    if text[brIndex + 1] == "random":
                        lampState['brightness'] = float(random.uniform(0,1))


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

def hsvInc(prev):
    if prev + INTERVAL >= 1.0:
        return 1.0
    return prev + INTERVAL

def hsvDec(prev):
    if prev - INTERVAL <= 0.0:
        return 0.0 
    return prev - INTERVAL

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
        queryList = query.split()
        parseText(queryList)
    except sr.UnknownValueError:
        query = "failed"
    print(query)




#parseText("hue random  25  saturation random  brightness random  decrease increase lamp reedd".split())

while True:
    recordCommand()

