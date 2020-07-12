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
letters = list("EPB") # Possible stimulus characters to be displayed
keys = ['e', 'p', 'b', 'space'] # Keypresses to listen for 
angles = [5, 10, 15, 20, 25, 30, 35, 40] # Retinal eccentricity (opening angle) values to test
directions = [0, 2] # 0 = Right (0°), 2 = Left (180°)
trials = 1 # Number of trails to run

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
    expName = 'Isolated Character'
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
        csvOutput(["Direction","Letter Height (degrees)", "Eccentricity (degrees)"]) 

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

# Calculates the height and angle in cm for a stimulus character, as well as the 
# x and y coordinates, given the display angle, direction, and size (in degrees)
def calculateDisplayCoords(trialInfo, displayInfo): 
    # Stimulus height in cm
    sizeCm = angleCalc(trialInfo['size'])
    angleCm = angleCalc(trialInfo['angle'])
    displayInfo['heightCm'] = sizeCm*heightMult

    displayInfo['xPos'] = centerX
    # Stimulus display x position
    if trialInfo['dir'] == 0:
        displayInfo['xPos'] += angleCm*rightXMult
    elif trialInfo['dir'] == 2:
        displayInfo['xPos'] += angleCm*leftXMult
    
    # Stimulus display y position
    displayInfo['yPos'] = 0
    # Set color to white
    displayInfo['color'] = 'white'
    return displayInfo
    
# Staircase algorithm which determines when to end a trial (identifies the 
# threshold identifiable letter height)
def stairCase(trialInfo):
    # Increment the number of responses recorded from the subject
    trialInfo['responses'] += 1
    
    # Reset numReversals if there are two sequential correct or incorrect 
    # answers. Update the number of total reversals
    if trialInfo['numReversals'] > 0 and trialInfo['lastResponse'] == trialInfo['thisResponse']:
        trialInfo['totalReversals'] += trialInfo['numReversals']
        trialInfo['numReversals'] = 0
    
    # If the subject correctly identified the stimulus character, decrease the 
    # size of the stimulus character 
    if trialInfo['thisResponse']:
        if trialInfo['numReversals'] == 0 and trialInfo['size'] > 1:
            # Decrease display size rapidly until an incorrect identification is 
            # made (while the size is > 1°)
            trialInfo['size'] -= 0.5 
        elif(trialInfo['size'] > 0.5):
            # Reduce the display size change decrement to 0.2 if the 
            # size is < 0.5°
            trialInfo['size'] -= 0.2 
        else:
            # Once a reversal has been made (after the first incorrect 
            # identification), decrease size by 0.1°
            trialInfo['size'] -= 0.1 
    # If the subject incorrectly identified the stimulus character, increase the 
    # size of the stimulus character
    else:
        trialInfo['numReversals'] += 1 # Increment the number of reversals recorded
        # If the current display size is greater than 0.5°, increase it by 0.2°
        if trialInfo['size'] > 0.5: 
            trialInfo['size'] += 0.2
        else:  # Otherwise, increase it by 0.1°
            trialInfo['size'] += 0.1 
            
    # Staircase algorithm convergence. Conditions for convergance: 3 or more 
    # consecutive reversals, 15 or more total reversals, 25 or more responses. 
    # If one of these conditions is met, the staircase converges and returns 
    # true. The letter height of the last correctly identified stimulus 
    # character is recorded as the threshold letter height
    if trialInfo['numReversals'] >= 3 or trialInfo['responses'] >= 25 or trialInfo['totalReversals'] > 15:
        trialInfo['stairCaseCompleted'] = True
    
    # If the display size has been lowered to > 0.1°, set it to 0.1°, because 
    # the monitor used in our experiment was unable to clearly display 
    # characters smaller than that size
    if trialInfo['size'] < 0.1:
        trialInfo['size'] = 0.1
        
    return trialInfo

# Returns a boolean indicating whether or not the subject's input matched the 
# stimulus character
def checkResponse(response, letter):
    if response[0] == 'escape':
        endExp()
    return (response[0] == letter.lower())

def instructions():
    # Display experiment instructions, end the experiment if the subject presses the esc key
    genDisplay({'text': 'Press the key corresponding to the character',\
        'xPos': 0, 'yPos': 5, 'heightCm': 1.5, 'color': 'white'}).draw()
    genDisplay({'text': 'displayed in the periphery (e, p, b),',\
        'xPos': 0, 'yPos': 3, 'heightCm': 1.5, 'color': 'white'}).draw()
    genDisplay({'text': 'or space bar if you absolutely can not read it',\
    'xPos': 0, 'yPos': 1, 'heightCm': 1.5, 'color': 'white'}).draw()
    genDisplay({'text': 'Press spacebar to continue',\
        'xPos': 0, 'yPos': -2, 'heightCm': 1.5, 'color': 'white'}).draw()
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
        
# Create a display object for the center dot
def genDot():
    return genDisplay({'text': '.', 'xPos': centerX, 'yPos': centerY,\
        'heightCm': 1.7*heightMult, 'color': 'lawngreen'})
        
def newTrialInfo(angle, direc, sz):
    trialInfo = {'numReversals': 0,\
        'totalReversals': 0,\
        'responses': 0,\
        'thisResponse': False,\
        'lastResponse': False,\
        'stairCaseCompleted': False,\
        'angle': angle,\
        'dir': direc,\
        'size': sz} 
    return trialInfo

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
    sz = (angles[int(pair/10)])/10
    if(sz < 1): # Ensure initial letter height is not 0
        sz = 1
    return newTrialInfo(angle, direc, sz)


dot = genDot()
instructions()

pairs = genPairs()

run = 0 # Store the number of trials completed
for pair in pairs: # Loop through the list of pairs
    
    trialInfo = interpretPair(pair)
    if not inBounds(trialInfo):
        continue
    
    # Continue to display the stimulus character and wait for subject input
    # until the staircase algorithm converges
    while not trialInfo['stairCaseCompleted']:
        # Choose a random letter to display
        displayInfo = {'text': random.choice(letters)}
        # Calculate display coordinates for the stimulus character
        displayInfo = calculateDisplayCoords(trialInfo, displayInfo)
        # Generate a display object for the stimulus character
        displayText = genDisplay(displayInfo)
        
        # Display a blank screen with only the center dot on the first stimulus presentation in the trial
        if trialInfo['responses'] == 0:
            dot.draw()
            win.flip()
            
        time.sleep(0.5)
        
        # Display the stimulus character and the center green dot. Every 0.05 
        # seconds, hide/display the dot to create a flashing effect
        flash = False # Whether or not to display the dot
        while 1:
            flash = (flash == False) # Reverse the value of flash
            if flash:
                dot.draw() # Draw the green dot
            displayText.draw() # Draw the stimulus character
            
            win.flip() # Update the display
            
            # Pause execution for 0.05 seconds and listen for keypress
            response = waitKeys(keyList = ['e', 'p', 'b', 'space', 'escape'], maxWait = 0.05, clearEvents = False)
            if response:
               break # Break if a keypress was detected
        
        trialInfo['lastResponse'] = trialInfo['thisResponse']
        # Check whether or not the input matched the stimulus character
        trialInfo['thisResponse'] = checkResponse(response, displayInfo['text'])
            
        # Call the staircase algorithm
        trialInfo = stairCase(trialInfo)
        
        # If the staircase has converged, output the data to the csv file
        if trialInfo['stairCaseCompleted'] and not fileName is None:
            # Write direction, threshold letter height, and retinal
            # eccentricity to csv. Direction is stored in the csv in the 
            # range of 1->4, rather than 0->3
            output = [(trialInfo['dir']+1), trialInfo['size'], trialInfo['angle']]
            csvOutput(output) 
    
    run += 1 # Increment the number of runs completed

    # Halfway through the trial, give the subject a 30 second break and display 
    # a countdown timer on the screen
    if len(dirExclusions) == 0 and run == (int(len(pairs)/2)):
        expBreak()

# End the experiment after all eccentricity/direction pairs have been completed
endExp()
