### Setup commands:
```
sudo pip3 install SpeechRecognition
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo 
pip3 install pyaudio
sudo apt-get install flac
sudo ln -s /home/pi/lampi-voice/lamp_voice.conf /etc/supervisor/conf.d/lamp_voice.conf
```


### Setup Instructions:
Attach the Microphone and run the following code in the Python shell
```python
import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
```
Locate the Input microphone you want to use and its `device_index`. Paste the device index into the `voiceLampi.py` file, at line 16


### Command Guide:
To change the lamp's state, the keyword "lamp" must be said first.

To toggle the power of the lamp, the following commands need to be used:
* "lamp on" or "lamp turn on"
* "lamp off" or "lamp turn off"

###

To change the color of the lamp, the following phrase must be said (to change the lamp to **BLUE** for example)

  **BLUE** - "lamp blue" or "lamp set blue"
  
Other colors included are as follows:  **RED**, **YELLOW**, **PURPLE**, **GREEN**, **ORANGE**, and others found in commands.txt
  
###

To change the brightness, hue, and saturation individually, the following can be used:

**Incrementing Change**
* "Lamp brightness up" or "Lamp brightness increase"
* "Lamp saturation up" or "Lamp saturation increase"

**Setting Characteristic**
* "Lamp saturation 30"
* "Lamp hue 75"

              
  
