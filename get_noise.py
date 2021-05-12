import math
import sys
import threading
import time
import wave
import urllib3
import requests
import socket

from contextlib import contextmanager
from ctypes import *

import RPi.GPIO as GPIO
import pyaudio
from scipy.io.wavfile import read

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


print(requests.__version__)



HOST = '0.0.0.0'
PORT = 5000

recording_time_in_seconds = 3
wav_output_file = 'output.wav'
normal_decibel_threshold = 35
loud_decibel_threshold = 50
extra_decibel_threshold = 75
led_pin = 17



def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(led_pin, GPIO.OUT)

def turn_off_led():
    # Turn off all LEDs
    GPIO.output(led_pin, GPIO.LOW)

def turn_on_led():
    GPIO.output(led_pin, GPIO.HIGH)

@contextmanager
def _no_alsa_err():
    # Function needed to suppress pyaudio warnings that appear on Raspberry Pi
    _ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

    def _py_error_handler(filename, line, function, err, fmt):
        pass

    _c_error_handler = _ERROR_HANDLER_FUNC(_py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(_c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

def get_mean(array):
    return sum(array) / len(array)


def record_audio(
        chunk=1024,
        audio_format=pyaudio.paInt16,
        channels=2,
        rate=44100):
    # Records an audio of record_seconds length and saves it
    with _no_alsa_err():
        p = pyaudio.PyAudio()
    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("\n- recording...")

    turn_on_led()

    frames = []
    for i in range(0, int(rate / chunk * recording_time_in_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("- done recording!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(wav_output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(audio_format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    turn_off_led()


def mean_decibel_level():
    x, wav_data = read(wav_output_file)
    mean_channels_squared = [get_mean(part) ** 2 for part in wav_data]
    return int(20 * math.log10(math.sqrt(get_mean(mean_channels_squared))))

def checkThreshold(conn, average_decibel):
    if average_decibel> normal_decibel_threshold and average_decibel<loud_decibel_threshold:
        conn.send(b'Not great, not terrible noise')
    elif average_decibel>loud_decibel_threshold and average_decibel<extra_decibel_threshold:
        conn.send(b'Come on man, why so noisy?')
    elif average_decibel>extra_decibel_threshold:
        conn.send(b'BEWARE! The room is extra extra noisy, your neighbours will get angry.')
    else:
        conn.send(b'it is quiet')

def run(conn):
    # Main function
    setup()
    while True:
        record_audio()
        decibel_level = mean_decibel_level()

        print('Average decibel recorded fr: {0}'.format(decibel_level))
        checkThreshold(conn, decibel_level)
        time.sleep(10)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('listening...')
    conn, addr = s.accept()
    print('accepted...')
    with conn:
        print('Connected by', addr)
        run(conn)
