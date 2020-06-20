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

def getDimensions():
        
    tvInfo = {'Width (px)': '3840', 'Height (px)': '2160', 'Width (cm)': '122.88'}
    
    # Input dialogue: session type, subject code
    dlg = gui.DlgFromDict(dictionary=tvInfo, sortKeys=False, title='TV Info')
    if dlg.OK == False:
        core.quit()
        
    return tvInfo

tvInfo = getDimensions()
tvInfo['height'] = 1.3

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=-1, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
        
# Initialize keyboard for subject input
keyPress = keyboard.Keyboard(bufferSize = 1, waitForStart = True)

green = [.207, 1, .259]

# Returns a displayText object with the given text, coordinates, height, color
def genDisplay(displayInfo):
    displayText = visual.TextStim(win=win,
    text= displayInfo['text'],
    font='Arial',
    pos=(displayInfo['xPos'], displayInfo['yPos']),
    height=displayInfo['heightCm'],
    wrapWidth=500,
    ori=0, 
    color=displayInfo['color'],
    colorSpace='rgb',
    opacity=1, 
    languageStyle='LTR',
    depth=0.0)
    return displayText
    
# Returns a displayText object for the center dot
def genDot(color):
    return genDisplay({'text': '.', 'xPos': 0, 'yPos': 0, 'heightCm': 1.7, 'color': color})
    
def checkHeightResponse(info):
    if info['thisResponse'] == 'down' and info['lastResponse'] == 'up':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'up':
        info['adjuster'] += info['increment']
    else:
        info['adjuster'] -= info['increment']
    return info 
    
def setHeight():
    heights = [1, 3, 7, 10]
    final = 0
    for height in heights:
        
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the I is', 'heightCm': 2, 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': str(height) + 'centimeters tall', 'heightCm': 2, 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (height*info['adjuster']), 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            
            keys = []
            keyPress.start()
            while len(keys) == 0:
                time.sleep(0.5)
                keys = keyPress.getKeys()
            #while len(keys) == 0:
             #  time.sleep(0.5)
              # keys = keyPress.getKeys()
            
            info['thisResponse'] = keys[0].name
            
            info = checkHeightResponse(info)
            
        final += info['adjuster']/height
    tvInfo['height'] = final/(len(heights))

def checkCenterResponse(info):
    if info['response'] == 'space':
        info['complete'] = True 
    elif info['response'] == 'up':
        info['y'] += 0.1
    elif info['response'] == 'down':
        info['y'] -= 0.1
    elif info['response'] == 'left':
        info['x'] -= 0.1
    elif info['response'] == 'right':
        info['x'] += 0.1
    return info 
    
def setDotCenter():
    info = {'x': 0, 'y': 0, 'complete': False}
    while not info['complete']:
            
        genDisplay({'text': 'Use the arrow keys to move the dot. Press spacebar once the dot is centered on the E', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
        genDisplay({'text': 'E', 'heightCm': (1*tvInfo['height']), 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
        genDisplay({'text': '.', 'heightCm': (1.7*tvInfo['height']), 'xPos': info['x'], 'yPos': info['y'], 'color': 'lawngreen'}).draw()
            
        win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
        win.flip()
            
        keys = []
        while len(keys) == 0:
            time.sleep(0.5)
            keys = keyPress.getKeys()
            
        info['response'] = keys[0].name
            
        info = checkCenterResponse(info)
            
    tvInfo['centerx'] = info['x']
    tvInfo['centery'] = info['y']

def setCenter():
    heights = [0.5, 3, 7, 10, 15]
    finalx, finaly = 0, 0
    
    for height in heights:
        
        info = {'x': 0, 'y': 0, 'complete': False}
        while not info['complete']:
            
            genDisplay({'text': 'Use the arrow keys to move the E. Press spacebar once the E is centered on the dot', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': 'E', 'heightCm': (height*tvInfo['height']), 'xPos': (0+info['x']), 'yPos': (0+info['y']), 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (1.7*tvInfo['height']), 'color': 'lawngreen'}).draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            
            info['response'] = keys[0].name
            
            info = checkCenterResponse(info)
            
        finalx += info['x']/height
        finaly += info['y']/height
    tvInfo['centerxmult'] = finalx/len(heights)
    tvInfo['centerymult'] = finaly/len(heights)
    
def checkRightResponse(info):
    if info['thisResponse'] == 'left' and info['lastResponse'] == 'right':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'right':
        info['adjuster'] += info['increment']
    else:
        info['adjuster'] -= info['increment']
    return info 
    
def setRight():
    angles = [2, 5, 10, 15, 20]
    final = 0
    
    for angle in angles:
        
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': str(angle) + 'centimeters to the right of the center dot', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': ((angle*info['adjuster'])+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (1.7*tvInfo['height']), 'color': 'lawngreen'}).draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            
            info['response'] = keys[0].name
            
            info = checkRightResponse(info)
            
        final += info['adjuster']/angle
    tvInfo['rightx'] = final/len(angles)
    
def setRightEdge():

    info = {'adjuster': 0, 'increment': 5, 'lastResponse': None, 'thisResponse': None,'complete': False}
    while not info['complete']:
            
        genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
        genDisplay({'text': 'at the right edge of the screen', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
        genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': (info['adjuster']+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
            
        win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
        win.flip()
            
        keys = []
        while len(keys) == 0:
            time.sleep(0.5)
            keys = keyPress.getKeys()
        info['lastResponse'] = info['thisResponse']
        info['thisResponse'] = keys[0].name
            
        info = checkRightResponse(info)
            
    tvInfo['rightEdge'] = info['adjuster']/tvInfo['rightx']
    
    
def checkLeftResponse(info):
    if info['thisResponse'] == 'right' and info['lastResponse'] == 'left':
        info['increment'] = info['increment']/2
    if info['thisResponse'] == 'space':
        info['complete'] = True
    elif info['thisResponse'] == 'left':
        info['adjuster'] += info['increment']
    else:
        info['adjuster'] -= info['increment']
    return info 
    
def setLeft():
    angles = [2, 5, 10, 15, 20]
    final = 0
    
    for angle in angles:
        
        info = {'adjuster': -(tvInfo['rightx']), 'increment': -0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': str(angle) + 'centimeters to the left of the center dot', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': ((angle*info['adjuster'])+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (1.7*tvInfo['height']), 'color': 'lawngreen'}).draw()
            
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip()
            
            keys = []
            while len(keys) == 0:
               time.sleep(0.5)
               keys = keyPress.getKeys()
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = keys[0].name
            
            info = checkLeftResponse(info)
            
        final += info['adjuster']/angle
    tvInfo['leftx'] = final/len(angles)
    
def setLeftEdge():

    info = {'adjuster': 0, 'increment': -5, 'lastResponse': None, 'thisResponse': None,'complete': False}
    while not info['complete']:
            
        genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
        genDisplay({'text': 'at the left edge of the screen', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
        genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': (info['adjuster']+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
            
        win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
        win.flip()
            
        keys = []
        while len(keys) == 0:
            time.sleep(0.5)
            keys = keyPress.getKeys()
        info['lastResponse'] = info['thisResponse']
        info['thisResponse'] = keys[0].name
            
        info = checkLeftResponse(info)
            
    tvInfo['leftEdge'] = info['adjuster']/tvInfo['leftx']

    
setHeight()
setDotCenter()
setCenter()
setRight()
setLeft()
    
fileName = os.path.join(os.getcwd(), 'monitor_calibration.csv')
    
csvOutput(list(tvInfo.keys()), fileName)
csvOutput(list(tvInfo.values()), fileName)
    
win.flip() 
logging.flush()
win.close()
core.quit()
    
