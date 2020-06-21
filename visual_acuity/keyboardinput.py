
from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
import numpy as np  
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os, sys, time, random, math
#from lib import *
'''
keyPress = keyboard.Keyboard()
print('starting')
i = 0
while i < 100:
    keys = []
    while keys is None or len(keys) == 0:
        print('waiting')
        time.sleep(1)
        keys = keyPress.getKeys()
        print(keys)
        if keys is None and len(keys) == 0:
            continue
    if keys[0] == 'escape':
        core.quit()
    key = keys[0]
    print(key.name)
    time.sleep(1)
    i += 1
'''
kb = keyboard.Keyboard()
def getKeyboardInput():
    kb.clearEvents(eventType='keyboard')
    keys = []
    while len(keys) == 0:
        core.wait(0.5)
        keys = kb.getKeys()
    if keys[0].name == 'escape':
        core.quit()
    return keys[0].name


for i in range(50):
    print(getKeyboardInput())
core.quit()