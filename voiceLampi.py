import subprocess
import json
import os
import time
import signal
import speech_recognition as sr
import paho.mqtt.client as MQTT
from lamp_common import *


MQTT_CLIENT_ID = "voice"


lampState = {}

def audioToText():
    #time.sleep(1)
    filename = "out.wav"
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
            print(text)
            parseText(text)
            #print(text)
        except:
            pass

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
  #  lampState = get_current_lamp_state()
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

    if "red" in text:
        lampState['color'] = {'h':1.0, 's': 1.0}
        lampState['on'] = True

    if "blue" in text:
        lampState['color'] = {'h':0.6, 's': 1.0}
        lampState['on'] = True


    if "green" in text:
        lampState['color'] = {'h':0.35, 's': 1.0}
        lampState['on'] = True

    if "yellow" in text:
        lampState['color'] = {'h':0.2, 's': 1.0}
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
    c.publish(TOPIC_SET_LAMP_CONFIG, json.dumps(lampState).encode('utf-8'), qos=1)
    time.sleep(0.1)
    print("published")
    c.loop_stop()

#parseText("red")

while(True):
    #proc_args = ['arecord', '-D' , 'dmic_sv' , '-c2' , '-r' , '44100' , '-f' , 'S32_LE' , '-t' , 'wav' , '-V' , 'mono' , '-v' , 'subprocess1.wav']
    proc_args = ['arecord', '-c1' , '--rate' , '44100' , '-f' , 'S16_LE' , '-t' , 'wav' , '-V' , '-v' , 'out.wav']
    rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)
    print("startRecordingArecord()> rec_proc pid= " + str(rec_proc.pid))
    #print("startRecordingArecord()> recording started")

    time.sleep(5)
    os.killpg(rec_proc.pid, signal.SIGTERM)
    rec_proc.terminate()
    rec_proc = None
    #print("stopRecordingArecord()> Recording stopped")
    audioToText()

