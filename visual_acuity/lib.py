from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
import numpy as np  
from numpy.random import shuffle
import os, sys, time, random, math, csv

# Opens the csvFile and writes the output argument specified by to the file
def csvOutput(output, fileName):
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
    
# Create a csv file for data output and a folder to store it in
def createOutputFile(expName):
    datadlg = gui.Dlg(title='Record Data?', pos=None, size=None, style=None,\
        labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
    ok_data = datadlg.show()
    if not datadlg.OK:
        return None
    
    # Change directory to script directory
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    
    # Store info about experiment, get date
    date = time.strftime("%m_%d")
    expInfo = {'Subject Name': ''}
    
    # Input dialogue: session type, subject code
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()
    
    # Create folder for data file output (cwd/Analysis/Data/<type>/<subject code>)
    OUTPATH = os.path.join(os.getcwd(), 'Data')
    os.mkdir(OUTPATH) 
    
    # Output file name: <OUTPATH>/<subject code_data_expName.csv>
    fileName = os.path.join(OUTPATH, (expInfo['Subject Name'] + '_' + date +\
         '_' + expName + '.csv'))
    
    # Print column headers if the output file does not exist
    if not os.path.isfile(fileName):
        csvOutput(["Direction","Letter Height (degrees)",\
            "Eccentricity (degrees)"], fileName) 
            
    return fileName

# Create visual window - monitor setup is required beforehand, can be found in 
# psychopy monitor tab. Set window size to the resolution of your display monitor
def createPsychopyObjects():
    tvInfo = csvInput(os.path.join(os.getcwd(), 'monitor_dimensions.csv'))
    mon = monitors.Monitor('TV') # Change this to the name of your display monitor
    mon.setWidth(float(tvInfo['Width (cm)']))
    win = visual.Window(
        size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=-1, 
        winType='pyglet', allowGUI=True, allowStencil=False,
        monitor= mon, color='grey', colorSpace='rgb',
        blendMode='avg', useFBO=True, 
        units='cm')
        
    # Initialize keyboard for subject input
    keyPress = keyboard.Keyboard()
    
    return win, keyPress
    
# Returns a displayText object with the given text, coordinates, height, color
def genDisplay(displayInfo):
    displayText = visual.TextStim(win=displayInfo['win'],
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
def genDot(win, color):
    return genDisplay({'text': '.', 'xPos': 0, 'yPos': 1.1, 'heightCm': 4, 'color': color, 'win': win})

# Takes a value in the form of angle of visual opening and returns the 
# equivalent value in centimeters (based upon the distToScreen variable)
def angleCalc(angle, distToScreen):
    radians = math.radians(angle) # Convert angle to radians
    # tan(theta) * distToScreen ... opposite = tan(theta)*adjacent
    spacer = (math.tan(radians)*distToScreen) 
    return spacer
    
# Calculates the height and angle in cm for a stimulus character, as well as the 
# x and y coordinates, given the display angle, direction, and size (in degrees)
# IMPORTANT: the value of the spacingAdjustment variable is unique to the monitor 
# used in our experiment. It will likely need to be changed to achieve proper 
# stimulus display on another monitor. Trial and error. Similarly, the yOffset 
# values will likely need to be adjusted (this offset is used to make move the 
# character to be in line with the exact center of the screen)
def calculateDisplayCoords(trialInfo): 
    spacingAdjustment = 2.3378
    
    calibrationFile = os.path.join(os.getcwd(), 'monitor_calibration.csv')
    
    if os.path.isfile(valibrationFile):
        spacingAdjustment = csvInput(calibrationFile)
    else:
        spacingAdjustment = {'centerx': 0, 'centery': 0,'height': 1, 'rx': 1, 'lx': 1, 'ry': 1, 'ly': 1}
    
    # Stimulus height in cm
    displayInfo['heightCm'] = (angleCalc(trialInfo['size'])*spacingAdjustment['height']) 
    # Stimulus distance from the screen's center in cm
    displayInfo['angleCm'] = angleCalc(trialInfo['angle']) 
    # Stimulus display x position
    displayInfo['xPos'] = (dirXMult[trialInfo['dir']]*displayInfo['angleCm']) 
    # Stimulus display y position
    displayInfo['yPos'] = (dirYMult[trialInfo['dir']]*displayInfo['angleCm']) + yOffset[trialInfo['dir']] 
    # Set color to white
    displayInfo['color'] = 'white'
    
    return displayInfo

# Returns a boolean indicating whether or not the subject's input matched the 
# stimulus character
def checkResponse(response, letter):
    return (response[0] == letter.lower())
    
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

# Generate a randomized list of angle and direction pairs. Each pair is 
# represented as a single integer. The index of the angle (in the angles array) 
# is multiplied by 10, and the index of the direction (in the directions array) 
# is added to it. Positive values represent horizontal pairs, and negative 
# represent vertical.
def genPairs(angles, directions):
    pairs = list(range(0))
    for i in range(trials):
        for j in range(len(angles)): # Loop through angles
            for k in range(len(directions)): # Loop through directions
                # Append (angle index * 10) + direction index to pairs
                pairs.append((j*10)+k) 
    shuffle(pairs) # Randomize the pairs list
    return pairs

# Display the instructions and wait for a keypress
def instructions(dispInfo):
    genDisplay(dispInfo).draw()
    dispInfo['win'].flip()
    # Wait until the subject presses a key
    theseKeys = event.waitKeys(keyList = ['space', 'escape'], clearEvents = False) 
    if theseKeys[0] == 'escape': # Quit the experiment if the subject presssed escape
        return False 
    return True 

# give the subject a 30 second break and display 
# a countdown timer on the screen
def expBreak(win):
    dispInfo = {'text': 'Break', 'xPos': 0, 'yPos': 0, 'heightCm': 5, 'color': 'white', 'win': win}
    breakText = genDisplay(dispInfo)
    dispInfo = {'text': 'Seconds', 'xPos': +2, 'yPos': -5, 'heightCm': 5, 'color': 'white', 'win': win}
    secondsText = genDisplay(dispInfo)
    dispInfo = {'text': 0, 'xPos': -11, 'yPos': -5, 'heightCm': 5, 'color': 'white', 'win': win}
    for i in range(30):
        win.clearBuffer()
        breakText.draw()
        secondsText.draw()
        dispInfo['text'] = str(30-i)
        genDisplay(dispInfo).draw()
        win.flip()
        time.sleep(1)