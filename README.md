# Noise Level Monitoring

## Overview

Our application detects if the room you are in is too noisy or not via a USB Microphone. If the threshold level is over 50 the configured user will receive a notification with "Not great, not terrible noise", If the threshold level is over 60 he will receive a notification with "Come on man, why so noisy?" and if the threshold level is over 70 the message will change to "BEWARE! The room is extra extra noisy, your neighbours will get angry."


## Demo
The Demo for our application can be seen here: 

https://user-images.githubusercontent.com/61203639/117950001-67174800-b31b-11eb-8516-6313f2896e7c.mp4


The project works as follows:
<ul>
    <li> First you run the python file. </li>
    <li> You run the flutter application on your phone and wait. </li>
    <li> The raspberry pi will record for 3 seconds and you will see the led turned on while recording.</li>
    <li> You will receive a notification with a personalised message depending on the threshold level reached. </li>
    <li> After that the raspberry pi will wait 10 seconds and the repeat the process.</li>
</ul>


![gif (1)](https://user-images.githubusercontent.com/61203639/117943488-d9385e80-b314-11eb-8037-b8eb3ffe3134.gif)



## Some pictures

![185253070_806707979970540_4719815854504411304_n](https://user-images.githubusercontent.com/61203639/117943912-49df7b00-b315-11eb-9f1a-9484925d36c2.jpg)

![184996524_1194202384372095_497042096130433693_n (1)](https://user-images.githubusercontent.com/61203639/117943925-4e0b9880-b315-11eb-8884-77f4093251e2.jpg)



## Schema
![ProjectSchema](https://user-images.githubusercontent.com/61203639/117864313-50321080-b29d-11eb-8529-def3ce1986bc.png)


## Pre-requisites
<ul>
    <li> A Raspberry Pi (We used a Raspberry Pi 4) but any Raspberry Pi with usb port can work  </li>
    <li> One led </li>
    <li> One resistor </li>
    <li> One breadboard with 830 points </li>
    <li> Hook-up cables female to male </li>
    <li> USB Microphone </li>
</ul>

## Setup and run
1. First you will need a micro SD which needs to be bootable. For flashing the micro SD you can use balenaEtcher https://www.balena.io/etcher/.
2. Connect the components, the led, the resistor and the wires to the breadboard and to the raspberry   from the pre-requisites as you see in the schema above.
3. Connect the USB Microphone to the USB port to the Raspberry Pi and then plug it in.
4. Configure your raspberry pi so that you can use it remotely. Enable the `ssh` and the `vnc` from raspi-config. Install also VNC viewer on your laptop or computer and enter the ip from your raspberry pi. You can also work directly on the raspberry pi with a mouse, a keyboard and a screen. 
5. Clone this repository on your raspberry pi (for the flutter application you can clone it on your laptop and run it on your phone)
6. Make sure you have pyhton3 installed. If you don't, then install it via `sudo apt install python3`.
7. For using the microphone with the raspberry pi you will need to follow this steps:<br>
        7.1. `nano /home/pi/.asoundrc` <br>
        7.2. Add this to the file above: <br>
```
pcm.!default {
  type asym
  capture.pcm "mic"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:3,0"
  }
}
```
<br>
8. You will need to install this packages : scipy and pyaudio with `pip3 install scipy` and `pip3 install pyaudio`

9. After you completed all the steps from above you just have to run the file get_noise.py with `python3 get_noise.py` and you are ready to go! 
You can now see if your neighbours hate you or not ;) !


## Optional 

You can make the Noise level detection script autorun at the start-up of the Raspberry Pi by adding the following line to the end of the /etc/rc.local file: `python3 get_noise.py`

## Team Members
<ul>
<li> Denisa Luca </li>
<li> Andreea-Cristina Korodi </li>
<li> Georgiana Loba </li>
</ul>
