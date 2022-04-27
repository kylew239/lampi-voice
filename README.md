### Setup commands:
```
sudo pip3 install SpeechRecognition
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo 
pip3 install pyaudio
sudo apt-get install flac
```


### Setup Instructions:
Attach the Microphone and run the following code in the Python shell
```python
import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
```
Locate the Input microphone you want to use and its `device_index`. Paste the device index into the `voiceLampi.py` file, at line 11