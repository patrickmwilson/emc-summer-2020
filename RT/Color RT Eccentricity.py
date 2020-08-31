# Isolated Character
#
# Displays a single character in the peripheral region for the subject to 
# identify. To see a photo of this experiment, open the 'ic.png' file within 
# the 'Protocol Pictures' folder
from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
from psychopy.event import waitKeys
import numpy as np  
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os, sys, time, random, math, csv


# Experimental variables
angles = [5, 10, 15, 20, 25, 30, 35, 40] # Retinal eccentricity (opening angle) values to test
directions = [0, 2] # 0 = Right (0°), 2 = Left (180°)
colors = ['red', 'green', 'blue', 'yellow']
trials = 50 # Number of trails to run

# Opens the csvFile and writes the output argument specified by to the file
def csvOutput(output):
    with open(fileName,'a', newline ='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()
    
# Opens the csvFile and returns the values stored within as a dictionary
def csvInput(fileName):
    with open(fileName) as csvFile:
        reader = csv.DictReader(csvFile, delimiter = ',')
        dict = next(reader)
    csvFile.close()
    return dict

# Change directory to script directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
fileName = os.path.join(os.getcwd(), 'monitor_calibration.csv')
if not os.path.isfile(fileName):
    print('You must run the calibration.py script to set up your monitor')
    time.sleep(5)
    core.quit()
    
tvInfo = csvInput(os.path.join(os.getcwd(),'monitor_calibration.csv'))

distToScreen = float(tvInfo['Distance to screen']) # Distance between the subject and the screen in centimeters
heightMult, spacer = float(tvInfo['height']), float(tvInfo['spacer'])
circleMult = float(tvInfo['circleRadius'])
centerX, centerY = float(tvInfo['centerx']), float(tvInfo['centery'])
rightXMult, leftXMult = float(tvInfo['rightx']), float(tvInfo['leftx'])
rightEdge, leftEdge = float(tvInfo['rightEdge']), float(tvInfo['leftEdge'])

# End the experiment: close the window, flush the log, and quit the script
def endExp():
    win.flip()
    logging.flush()
    win.close()
    core.quit()

# Input dialogue: record data to csv file?
datadlg = gui.Dlg(title='Record Data?', pos=None, size=None, style=None,\
     labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
ok_data = datadlg.show()
recordData = datadlg.OK

if recordData:
    # Store info about experiment, get date
    date = time.strftime("%m_%d")
    expName = 'Color RT Eccentricity'
    expInfo = {'Subject Name': ''}
    
    # Input dialogue: session type, subject code
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()
    
    # Create folder for data file output (cwd/Analysis/Data/<type>/<subject code>)
    OUTPATH = os.path.join(os.getcwd(), 'Data')
    if not os.path.isdir(OUTPATH):
        os.mkdir(OUTPATH)
    
    # Output file name: <OUTPATH>/<subject code_data_expName.csv>
    fileName = os.path.join(OUTPATH,\
        (expInfo['Subject Name'] + '_' + date + '_' + expName + '.csv'))
    
    # Print column headers if the output file does not exist
    if not os.path.isfile(fileName):
        csvOutput(["Color","Direction", "Eccentricity (degrees)", "Reaction Time (s)"]) 

# Input dialogue: directions to test
datadlg = gui.Dlg(title='Select dot position', screen=-1)
datadlg.addField('Position: ', choices = ["Center", "Right", "Left"])
ok_data = datadlg.show()
if ok_data is None:
    endExp()
elif ok_data[0] == 'Left':
    centerX = -(leftEdge-3)
    dirExclusions = [2]
elif ok_data[0] == 'Right':
    centerX = rightEdge-3
    dirExclusions = [0]
else:
    dirExclusions = []

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=int(tvInfo['Screen number']), 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')

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
        

# Takes a value in the form of angle of visual opening and returns the 
# equivalent value in centimeters (based upon the distToScreen variable)
def angleCalc(angle):
    radians = math.radians(angle) # Convert angle to radians
    # tan(theta) * distToScreen ... opposite = tan(theta)*adjacent
    spacer = math.tan(radians)*distToScreen
    return spacer
    
# Returns a boolean indicating whether or not the subject's input matched the 
# stimulus character
def checkResponse(response, color):
    if response == 'escape':
        endExp()
        
    if response == 'c': 
        ans = 'red'
    elif response == 'v':
        ans = 'green'
    elif response == 'n':
        ans = 'blue'
    else:
        ans = 'yellow'
    
    return (ans == color)

def instructions():
    # Display experiment instructions, end the experiment if the subject presses the esc key
    genDisplay({'text': 'Press c if you see a red dot, v if you see a green dot,',\
        'xPos': 0, 'yPos': 5, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    genDisplay({'text': 'n if you see a blue dot, or m if you see a yellow dot',\
        'xPos': 0, 'yPos': 3, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    genDisplay({'text': 'Press spacebar to continue',\
        'xPos': 0, 'yPos': -2, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    win.flip()
    key = waitKeys(keyList = ['space', 'escape'])
    if key[0] == 'escape':
        endExp()
        
# give the subject a 30 second break and display 
# a countdown timer on the screen
def expBreak():
    dispInfo = {'text': 'Break', 'xPos': 0, 'yPos': 4, 'heightCm': 3, 'color': 'white'}
    breakText = genDisplay(dispInfo)
    dispInfo = {'text': '', 'xPos': 0, 'yPos': -1, 'heightCm': 3, 'color': 'white'}
    for i in range(30):
        breakText.draw()
        dispInfo['text'] = str(30-i) + ' seconds'
        genDisplay(dispInfo).draw()
        win.flip()
        time.sleep(1)

# Make sure that the current display coordinates are within the boundaries of the screen
def inBounds(trialInfo):
    if trialInfo['dir'] in dirExclusions:
        return False
    if trialInfo['dir'] == 0:
        if (centerX + angleCalc(trialInfo['angle'])) > rightEdge:
            return False 
    elif trialInfo['dir'] == 2:
        if (centerX - angleCalc(trialInfo['angle'])) < (-leftEdge):
            return False 
    return True
    
# Generate a randomized list of angle and direction pairs. Each pair is 
# represented as a single integer. The index of the angle (in the angles array) 
# is multiplied by 10, and the index of the direction (in the directions array) 
# is added to it. 
def genPairs():
    pairs = list(range(0))
    for i in range(trials):
        for j in range(len(angles)): # Loop through angles
            for k in range(len(directions)): # Loop through directions
                # Append (angle index * 10) + direction index to pairs
                pairs.append((j*10)+k) 
    shuffle(pairs) # Randomize the pairs list
    return pairs
    
def interpretPair(pair):
    # Initialize trial variables related to staircase algorithm
    angle = angles[int(pair/10)] # Angle index = pair/10
    direc = directions[int(pair%10)] # Direction index = pair%10
    color = random.choice(colors)
    
    return {'angle': angle, 'dir': direc, 'color': color}

cross = visual.ShapeStim(
    win=win, name='Cross', vertices='cross',units='deg', 
    size=(1, 1),
    ori=0, pos=(centerX, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)

circleRadius = angleCalc(2)*circleMult
circle = visual.Circle(win=win, radius=circleRadius, edges=32, lineColor = 'white', fillColor = 'white', pos = (0,0))


instructions()

pairs = genPairs()

run = 0 # Store the number of trials completed
for pair in pairs: # Loop through the list of pairs
    
    win.flip()
    
    trialInfo = interpretPair(pair)
    if not inBounds(trialInfo):
        continue
        
    time.sleep(2)
        
    cross.draw()
    
    win.flip()
    
    time.sleep(random.randint(10,15)/1000)
    
    win.flip()
    
    time.sleep(random.randint(3,8)/1000)
    
    circle.lineColor = trialInfo['color']
    circle.fillColor = trialInfo['color']
    
    angleCm = angleCalc(trialInfo['angle'])
    print(angleCm)
    
    xPos = centerX
    if trialInfo['dir'] == 0:
        xPos += angleCm*rightXMult
    elif trialInfo['dir'] == 2:
        xPos += angleCm*leftXMult
        
    circle.pos = (xPos, 0)
    
    circle.draw()
    
    times = {'start': 0, 'end': 0}

    win.timeOnFlip(times, 'start')

    win.flip()

    keys = event.waitKeys(timeStamped = True, keyList = ['c', 'v', 'n', 'm', 'escape'])

    key = keys[0]

    if key[0] == 'escape':
        endExp()

    times['end'] = key[1]
    
    reactionTime = times['end'] - times['start']
    
    if checkResponse(key[0], trialInfo['color']):
        csvOutput([trialInfo['color'], trialInfo['dir'], trialInfo['angle'], reactionTime])
    
    
    run += 1 # Increment the number of runs completed

    # Halfway through the trial, give the subject a 30 second break and display 
    # a countdown timer on the screen
    if len(dirExclusions) == 0 and run == (int(len(pairs)/2)):
        expBreak()

# End the experiment after all eccentricity/direction pairs have been completed
endExp()
