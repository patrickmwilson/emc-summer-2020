from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.hardware import keyboard
import os, time, csv

# Opens the csvFile and writes the output argument specified by to the file
def csvOutput(output, fileName):
    with open(fileName,'a', newline ='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()

info = {'Width (px)': '3840', 'Height (px)': '2160', 'Width (cm)': '122.88', 'Distance to screen (cm)': '50'}
# Input dialogue: session type, subject code
dlg = gui.DlgFromDict(dictionary=info, sortKeys=False, title='TV Info')
if dlg.OK == False:
    core.quit()
    
tvInfo = {'Width (px)': info['Width (px)'],\
    'Height (px)': info['Height (px)'],\
    'Width (cm)': info['Width (cm)'],\
    'Distance to screen (cm)':  info['Distance to screen (cm)'],\
    'height': 0,\
    'centerx': 0,\
    'centery': 0,\
    'centerxmult': 0,\
    'centerymult': 0,\
    'rightx': 0,\
    'rightEdge': 0,\
    'leftx': 0,\
    'leftEdge': 0}

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=-1, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
        
# Initialize keyboard for subject input
#kb = keyboard.Keyboard(bufferSize = 1)

dotSize = 5

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
    
def getKeyboardInput():
    keys = event.waitKeys()
    if keys[0] == 'escape':
        core.quit()
    return keys[0]

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
    
def setHeight(tvInfo):
    heights = [1, 3, 7, 10]
    for height in heights:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Press down arrow to reduce size, up arrow to increase. Press spacebar once the I is', 'heightCm': 2, 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': str(height) + ' centimeters tall', 'heightCm': 2, 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (height*info['adjuster']), 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            info['thisResponse'] = getKeyboardInput()
            info = checkHeightResponse(info)
        tvInfo['height'] += info['adjuster']/height
    tvInfo['height'] = tvInfo['height']/(len(heights))
    return tvInfo

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
    return info 
    
def setDotCenter(tvInfo):
    info = {'x': 0, 'y': 0, 'complete': False}
    while not info['complete']:
            
        genDisplay({'text': 'Use the arrow keys to move the dot. Press spacebar once the dot is centered on the A', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
        genDisplay({'text': 'A', 'heightCm': (1*tvInfo['height']), 'xPos': 0, 'yPos': 0, 'color': 'white'}).draw()
        genDisplay({'text': '.', 'heightCm': (dotSize*tvInfo['height']), 'xPos': info['x'], 'yPos': info['y'], 'color': 'lawngreen'}).draw()
        win.flip()
            
        info['response'] = getKeyboardInput()
        info = checkCenterResponse(info)
    tvInfo['centerx'], tvInfo['centery'] = info['x'], info['y']
    return tvInfo

def setCenter(tvInfo):
    heights = [0.5, 3, 7, 10, 15]
    for height in heights:
        info = {'x': 0, 'y': 0, 'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Use the arrow keys to move the E. Press spacebar once the E is centered on the dot', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': 'E', 'heightCm': (height*tvInfo['height']), 'xPos': (0+info['x']), 'yPos': (0+info['y']), 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (dotSize*tvInfo['height']), 'color': 'lawngreen'}).draw()
            win.flip()
            
            info['response'] = getKeyboardInput()
            info = checkCenterResponse(info)
        tvInfo['centerxmult'] += info['x']/height
        tvInfo['centerymult'] += info['y']/height
    tvInfo['centerxmult'] = tvInfo['centerxmult']/len(heights)
    tvInfo['centerymult'] = tvInfo['centerymult']/len(heights)
    return tvInfo
    
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
    
def setRight(tvInfo):
    angles = [2, 5, 10, 15, 20]
    for angle in angles:
        info = {'adjuster': 1, 'increment': 0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Arrow keys to move the I. Press spacebar once the center of the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': str(angle) + ' centimeters to the right of the center dot', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': ((angle*info['adjuster'])+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (dotSize*tvInfo['height']), 'color': 'lawngreen'}).draw()
            win.flip()
            
            info['lastResponse'] = info['thisResponse']
            
            info['thisResponse'] = getKeyboardInput()
            info = checkRightResponse(info)
        tvInfo['rightx'] += info['adjuster']/angle
    tvInfo['rightx'] = tvInfo['rightx']/len(angles)
    return tvInfo
    
def setRightEdge(tvInfo):
    info = {'adjuster': 0, 'increment': 5, 'lastResponse': None, 'thisResponse': None,'complete': False}
    while not info['complete']:
        genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
        genDisplay({'text': 'at the right edge of the screen', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
        genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': (info['adjuster']+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
        win.flip()
            
        info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
        info = checkRightResponse(info)
    tvInfo['rightEdge'] = (info['adjuster']/tvInfo['rightx']) -10
    return tvInfo
    
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
    
def setLeft(tvInfo):
    angles = [2, 5, 10, 15, 20]
    for angle in angles:
        info = {'adjuster': -(tvInfo['rightx']), 'increment': -0.1, 'lastResponse': None, 'thisResponse': None,'complete': False}
        while not info['complete']:
            genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
            genDisplay({'text': str(angle) + ' centimeters to the left of the center dot', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
            genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': ((angle*info['adjuster'])+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
            genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (dotSize*tvInfo['height']), 'color': 'lawngreen'}).draw()
            win.flip()
            
            info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
            info = checkLeftResponse(info)
        tvInfo['leftx'] += info['adjuster']/angle
    tvInfo['leftx'] = tvInfo['leftx']/len(angles)
    return tvInfo
    
def setLeftEdge(tvInfo):
    info = {'adjuster': 0, 'increment': -5, 'lastResponse': None, 'thisResponse': None,'complete': False}
    while not info['complete']:
        genDisplay({'text': 'Use the arrow keys to move the I. Press spacebar once the I is', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 10, 'color': 'white'}).draw()
        genDisplay({'text': 'at the left edge of the screen', 'heightCm': (2*tvInfo['height']), 'xPos': 0, 'yPos': 7, 'color': 'white'}).draw()
        genDisplay({'text': 'I', 'heightCm': (5*tvInfo['height']), 'xPos': (info['adjuster']+(5*tvInfo['centerxmult'])), 'yPos': (5*tvInfo['centerymult']), 'color': 'white'}).draw()
        win.flip()
            
        info['lastResponse'], info['thisResponse'] = info['thisResponse'], getKeyboardInput()
        info = checkLeftResponse(info)
    tvInfo['leftEdge'] = (info['adjuster']/tvInfo['leftx']) + 10
    return tvInfo

tvInfo = setHeight(tvInfo)
tvInfo = setDotCenter(tvInfo)
tvInfo = setCenter(tvInfo)
tvInfo = setRight(tvInfo)
tvInfo = setRightEdge(tvInfo)
tvInfo = setLeft(tvInfo)
tvInfo = setLeftEdge(tvInfo)

# Change directory to script directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
fileName = os.path.join(os.getcwd(), 'monitor_calibration.csv')
    
csvOutput(list(tvInfo.keys()), fileName)
csvOutput(list(tvInfo.values()), fileName)
    
win.flip() 
logging.flush()
win.close()
core.quit()