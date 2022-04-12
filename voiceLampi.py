import subprocess
import os
import time
import signal
import speech_recognition as sr

def textToSpeech():
    #time.sleep(1)
    filename = "out.wav"
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)

while(True):
    #proc_args = ['arecord', '-D' , 'dmic_sv' , '-c2' , '-r' , '44100' , '-f' , 'S32_LE' , '-t' , 'wav' , '-V' , 'mono' , '-v' , 'subprocess1.wav']
    proc_args = ['arecord', '-c1' , '--rate' , '44100' , '-f' , 'S16_LE' , '-t' , 'wav' , '-V' , '-v' , 'out.wav']
    rec_proc = subprocess.Popen(proc_args, shell=False, preexec_fn=os.setsid)
    #print("startRecordingArecord()> rec_proc pid= " + str(rec_proc.pid))
    #print("startRecordingArecord()> recording started")

    time.sleep(5)
    os.killpg(rec_proc.pid, signal.SIGTERM)
    rec_proc.terminate()
    rec_proc = None
    #print("stopRecordingArecord()> Recording stopped")
    textToSpeech()

def praseText(text):
    
