import subprocess
import json
import os
import time
import signal
import speech_recognition as sr
import paho.mqtt.client as MQTT
from lamp_common import *


MQTT_CLIENT_ID = "voice"


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
            parseText(text)
            print(text)
        except:
            pass



def parseText(text):
    c = MQTT.Client(client_id=MQTT_CLIENT_ID)
    c.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
                      keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
    c.loop_start()
    
    if "on" in text:
        print("ON IS FOUND")
        msg = {'color': {'h': 1.0, 's': 1.0},
               'brightness': 1.0,
               'on': True,
               'client': MQTT_CLIENT_ID}
        c.publish(TOPIC_SET_LAMP_CONFIG, json.dumps(msg).encode('utf-8'), qos=1)
        print("PUBLISHED")

    if "off" in text:
        print("OFF IS FOUND")
        msg = {'color': {'h': 1.0, 's': 1.0},
               'brightness': 1.0,
               'on': False,
               'client': MQTT_CLIENT_ID}
        c.publish(TOPIC_SET_LAMP_CONFIG, json.dumps(msg).encode('utf-8'), qos=1)

    time.sleep(0.1)
    c.loop_stop()

#parseText("on")

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

