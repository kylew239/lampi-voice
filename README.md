### Setup commands:
```
sudo pip3 install SpeechRecognition
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo 
pip3 install pyaudio
```


### Setup Instructions:
Attache Microphone and run "arecord -l"
Find the card number and device number of the Microphone you want to use
Run `nano ~/.asoundrc` and paste in the following code, making sure to update the card and device numbers

```python
pcm.!default {
        type hw
        card #
        device #
}

ctl.!default {
        type hw
        card #
        device #
}
```