# Monitor Calibration
#
# 

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
from lib import *

win = None 
keyPress = None
defaultKeyboard = None

# Spacing adjustments for text display - These are unique to the particular 
# monitor that was used in the experiment and would need to be modified 
# manually for correct stimulus display
dirXMult = [1.62, 0, -1.68, 0] # Multiply x position by this value
dirYMult = [0, -1.562, 0, 1.748] # Multiply y position by this value
yOffset = [0.2, 0, 0.2, 0] # Offset y position by this value

def checkCalibration():
    # Change directory to script directory
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    fileName = os.path.join(os.getcwd(), 'monitor_calibration.csv')
    return os.path.isfile(fileName)
    
def checkHeightResponse(info):
    if info['thisResponse'] == 'down' and info['lastResponse'] == 'up':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'up':
        info['adjuster'] = info['adjuster'] + info['increment']
    else:
        info['adjuster'] = info['adjuster'] - info['increment']
        
def setHeight(adjustments):
    heights = [5, 10, 15, 20]
    final = 0
    for height in heights:
        
        info = {'adjuster': 1, 'increment': 1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the I is', 'heightCm': 8, 'xPos': 0, 'yPos': 35, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': str(height), 'heightCm': 8, 'xPos': 0, 'yPos': 25, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'centimeters tall', 'heightCm': 8, 'xPos': 0, 'yPos': 15, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'I', 'heightCm': (height*adjuster), 'xPos': 0, 'yPos': 0, 'color': 'white', 'win': win}).draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            
            info['thisResponse'] = keys[0].name
            
            info = checkHeightResponse(info)
            
        final += info['adjuster']
    adjustments['height'] = final/(len(heights))

def checkCenterResponse(info):
    if info['response'] == 'space':
        info['complete'] = True 
    elif info['response'] == 'up':
        info['y'] += 0.05
    elif info['response'] == 'down':
        info['y'] -= 0.05
    elif info['response'] == 'left':
        info['x'] -= 0.05
    elif info['response'] == 'right':
        info['x'] += 0.05

def setCenter(adjustments):
    heights = [5, 10, 15, 20]
    finalx = 0, finaly = 0
    
    dot = genDot(win, [.207, 1, .259])
    for height in heights:
        
        info = {'x': 0, 'y': 0, 'complete': False}
        while not info['complete']:
            
            genDisplay({'text': 'Use the arrow keys to move the E. Press spacebar once the E is centered on the dot', 'heightCm': 8, 'xPos': 0, 'yPos': 35, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'E', 'heightCm': height, 'xPos': (0+info['x']), 'yPos': (0+info['y']), 'color': 'white', 'win': win}).draw()
            dot.draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            
            info['response'] = keys[0].name
            
            info = checkCenterResponse(info)
            
        finalx += info['x']
        finaly += info['y']
    adjustments['centerx'] = finalx/len(heights)
    adjustments['centery'] = finaly/len(heights)
    
def checkRightResponse(info):
    if info['thisResponse'] == 'left' and info['lastResponse'] == 'right':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'right':
        info['adjuster'] = info['adjuster'] + info['increment']
    else:
        info['adjuster'] = info['adjuster'] - info['increment']
    
def setRight(adjustments):
    angles = [5, 20, 30, 40, 50]
    final = 0
    
    dot = genDot(win, [.207, 1, .259])
    for angle in angles:
        
        info = {'adjuster': adjustments['rightx'], 'increment': 1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': 8, 'xPos': 0, 'yPos': 35, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': str(angle), 'heightCm': 8, 'xPos': 0, 'yPos': 25, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'centimeters to the right of the center dot', 'heightCm': 8, 'xPos': 0, 'yPos': 15, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'I', 'heightCm': 5, 'xPos': (angle*info['adjuster']), 'yPos': 0, 'color': 'white', 'win': win}).draw()
            dot.draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            
            info['response'] = keys[0].name
            
            info = checkRightResponse(info)
            
        final += info['adjuster']
    adjustments['rightx'] = final/len(angles)
    
    
def checkLeftResponse(info):
    if info['thisResponse'] == 'right' and info['lastResponse'] == 'left':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'left':
        info['adjuster'] = info['adjuster'] + info['increment']
    else:
        info['adjuster'] = info['adjuster'] - info['increment']
    
def setLeft(adjustments):
    angles = [5, 20, 30, 40, 50]
    final = 0
    
    dot = genDot(win, [.207, 1, .259])
    for angle in angles:
        
        info = {'adjuster': -(adjustments['rightx']), 'increment': -1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': 8, 'xPos': 0, 'yPos': 35, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': str(angle), 'heightCm': 8, 'xPos': 0, 'yPos': 25, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'centimeters to the left of the center dot', 'heightCm': 8, 'xPos': 0, 'yPos': 15, 'color': 'white', 'win': win}).draw()
            genDisplay({'text': 'I', 'heightCm': 5, 'xPos': (angle*info['adjuster']), 'yPos': 0, 'color': 'white', 'win': win}).draw()

            dot.draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = keys[0].name
            
            info = checkLeftResponse(info)
            
        final += info['adjuster']
    adjustments['leftx'] = final/len(angles)

def calibrate():
    
    tvInfo = {'Width (px)': '', 'Height (px)': '', 'Width (cm)': ''}
    
    # Input dialogue: session type, subject code
    dlg = gui.DlgFromDict(dictionary=tvInfo, sortKeys=False, title='TV Info')
    if dlg.OK == False:
        core.quit()
        
    csvOutput(os.path.join(os.getcwd(), 'monitor_dimensions.csv'), list(tvInfo.keys))
    csvOutput(os.path.join(os.getcwd(), 'monitor_dimensions.csv'), list(tvInfo.values))
    
    win, keyPress = createPsychopyObjects()
    
    adjustments = {'height': 1, 'centerx': 0, 'centery': 0, 'rightx': 1, 'leftx': -1}
    
    setHeight(adjustments)
    setCenter(adjustments)
    setRight(adjustments)
    setLeft(adjustments)
    
    csvOutput(os.path.join(os.getcwd(), 'monitor_calibration.csv'), list(adjustments.keys))
    csvOutput(os.path.join(os.getcwd(), 'monitor_calibration.csv'), list(adjustments.values))
    
    win.flip() 
    logging.flush()
    win.close()
    core.quit()
    
