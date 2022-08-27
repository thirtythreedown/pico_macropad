"""
Pi pico rotary encoder volume control with click support
Based on code and explanations from:
https://www.hackster.io/tyronwakeford/pico-macro-keyboard-and-volume-control-994cf5
https://lastminuteengineers.com/rotary-encoder-arduino-tutorial/
"""

import board
import usb_hid
import time
import digitalio
from digitalio import DigitalInOut, Direction
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

led = digitalio.DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

CLK_PIN = board.GP4
DT_PIN = board.GP3
SW_PIN = board.GP2
clk_last = None
sw_last = None
#totalMode = 3
currentMode = 2

cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

clk = digitalio.DigitalInOut(CLK_PIN)
clk.direction = digitalio.Direction.INPUT

dt = digitalio.DigitalInOut(DT_PIN)
dt.direction = digitalio.Direction.INPUT

sw = digitalio.DigitalInOut(SW_PIN)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

#def millis():
#    return time.monotonic() * 1000

def ccw():
    print("CCW")

    if(currentMode == 2):   # Volume decrement
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)

def cw():
    print("CW")
    if(currentMode == 2):     # Volume increment
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        
def mute():
    print("Mute")
    cc.send(ConsumerControlCode.MUTE)
    

while True:
#    print("The clk.value is" + str(clk.value))
#    print("The dt.value is" + str(dt.value))
    clkState = clk.value
    if(clk_last != clkState):
        if(dt.value != clkState):
            cw()
        else:
            ccw()
            
    clk_last = clkState
    
    swState = sw.value
    if sw_last != swState: #if button 1 pressed
        mute() #sending out code for 1
        time.sleep(0.2) #sleep for a spell
    sw_last = sw.value
        