from neopixel import Neopixel
from machine import Pin
import time

pixPin = 0
pixNum = 8
pix = Neopixel(pixNum, 0, Pin(pixPin), "RGB")
red=(255, 0, 0)
green=(0, 255, 0)

while True:
    for i in range(0, pixNum, 1):
        pix.fill(red)
        pix[i] = green
        pix.show()
        time.sleep(0.1)
