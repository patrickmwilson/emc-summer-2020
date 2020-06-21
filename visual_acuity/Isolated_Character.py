# Isolated Character
#
# Displays a single character in the peripheral region for the subject to 
# identify. 
from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
import os, sys, time, random, math, csv

from lib import *

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

# Change directory to script directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
fileName = os.path.join(os.getcwd(), 'monitor_calibration.csv')
if not os.path.isfile(fileName):
    disp('You must run the calibration.py script to set up your monitor')
    time.sleep(5)
    core.quit()
    
tvInfo = csvInput(os.path.join(os.getcwd(),'monitor_calibration.csv'))

# Experimental variables
letters = list("EPB") # Possible stimulus characters to be displayed
keys = ['e', 'p', 'b', 'space'] # Keypresses to listen for 
angles = [0, 5, 10, 15, 20, 25, 30, 35, 40] # Retinal eccentricity (opening angle) values to test
directions = [0, 2] # 0 = Right (0°), 2 = Left (180°)
distToScreen = 50 # Distance between the subject and the screen in centimeters
trials = 1 # Number of trails to run
green= [.207, 1, .259] # Defining green color for center dot

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

# End the experiment: close the window, flush the log, and quit the script
def endExp():
    win.flip()
    logging.flush()
    win.close()
    core.quit()

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=-1, 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
kb = keyboard.Keyboard

# Input dialogue: record data to csv file? If yes, create the csv file for data output
fileName = createOutputFile('Isolated Character')

datadlg = gui.Dlg(title='Record Data?', pos=None, size=None, style=None,\
    labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
ok_data = datadlg.show()
recordData = datadlg.OK
    
if recordData:
    # Change directory to script directory
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    
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
    os.mkdir(OUTPATH) 
    
    # Output file name: <OUTPATH>/<subject code_data_expName.csv>
    fileName = os.path.join(OUTPATH,\
        (expInfo['Subject Name'] + '_' + date + '_' + expName + '.csv'))
    
    # Print column headers if the output file does not exist
    if not os.path.isfile(fileName):
        csvOutput(["Direction","Letter Height (degrees)", "Eccentricity (degrees)"], fileName) 
        
def getKeyboardInput(keyL = None, loop = True, waitTime = 0.5):
    kb.clearEvents(eventType='keyboard')
    keys = []
    while 1:
        core.wait(waitTime)
        keys = kb.getKeys(keyList = keyL)
        if loop and len(keys) == 0:
            continue 
        break
    if len(keys) == 0:
        return None 
    elif keys[0].name == 'escape':
        core.quit()
    return keys[0].name
        
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
def genDot():
    return genDisplay({'text': '.', 'xPos': tvInfo['centerx'], 'yPos': tvInfo['centery'], 'heightCm': (1.7*tvInfo['height']), 'color': green})
    
# Takes a value in the form of angle of visual opening and returns the 
# equivalent value in centimeters (based upon the distToScreen variable)
def angleCalc(angle):
    radians = math.radians(angle) # Convert angle to radians
    # tan(theta) * distToScreen ... opposite = tan(theta)*adjacent
    spacer = (math.tan(radians)*tvInfo['Distance to screen']) 
    return spacer
    
# Calculates the height and angle in cm for a stimulus character, as well as the 
# x and y coordinates, given the display angle, direction, and size (in degrees)
# IMPORTANT: the value of the spacingAdjustment variable is unique to the monitor 
# used in our experiment. It will likely need to be changed to achieve proper 
# stimulus display on another monitor. Trial and error. Similarly, the yOffset 
# values will likely need to be adjusted (this offset is used to make move the 
# character to be in line with the exact center of the screen)
def calculateDisplayCoords(trialInfo, displayInfo): 
    # Stimulus height in cm
    displayInfo['heightCm'] = (angleCalc(trialInfo['size'])*tvInfo['height']) 
    # Stimulus display x position
    if trialInfo['dir'] == 0:
        displayInfo['xPos'] = angleCalc(trialInfo['angle'])*tvInfo['rightx']
    elif trialInfo['dir'] == 2:
        displayInfo['xPos'] = angleCalc(trialInfo['angle'])*tvInfo['leftx']
    displayInfo['xPos'] += tvInfo['centerxmult']*displayInfo['heightCm']
    # Stimulus display y position
    displayInfo['yPos'] = tvInfo['centerymult']*displayInfo['heightCm']
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
    
# give the subject a 30 second break and display 
# a countdown timer on the screen
def expBreak():
    dispInfo = {'text': 'Break', 'xPos': 0, 'yPos': 0, 'heightCm': 5, 'color': 'white'}
    breakText = genDisplay(dispInfo)
    dispInfo = {'text': 'Seconds', 'xPos': +2, 'yPos': -5, 'heightCm': 5, 'color': 'white'}
    secondsText = genDisplay(dispInfo)
    dispInfo = {'text': 0, 'xPos': -11, 'yPos': -5, 'heightCm': 5, 'color': 'white'}
    for i in range(30):
        win.clearBuffer()
        breakText.draw()
        secondsText.draw()
        dispInfo['text'] = str(30-i)
        genDisplay(dispInfo).draw()
        win.flip()
        core.sleep(1)
        
# Display the instructions and wait for a keypress
def instructions(dispInfo):
    genDisplay(dispInfo).draw()
    dispInfo['win'].flip()
    # Wait until the subject presses a key
    key = getKeyboardInput(keyL = ['space','escape'], loop = True)

# Display experiment instructions, end the experiment if the subject presses the esc key
dispInfo = {'text': '    Press the key corresponding to the character \n         displayed in the periphery, or space bar \n                        if you can not read it    \n\n                 Press spacebar to continue',\
    'xPos': 0, 'yPos': 5, 'heightCm': 5, 'color': 'white', 'win': win}
instructions(dispInfo):

dispInfo = {'text': '  Take some time to familiarize yourself with the keys\n\n                       Press spacebar to begin',\
    'xPos': 0, 'yPos': 0, 'heightCm': 5, 'color': 'white', 'win': win}
instructions(dispInfo):

# Generate display object for the green dot in the center of the screen
dot = genDot()

# Generate a list of angle and direction pairs to test
pairs = genPairs(angles, directions)
run = 0 # Store the number of trials completed
for pair in pairs: # Loop through the list of pairs
    
    # Initialize trial variables related to staircase algorithm
    trialInfo = {'numReversals': 0, 'totalReversals': 0, 'responses': 0,\
        'thisResponse': False, 'lastResponse': False, 'stairCaseCompleted': False,\
        'angle': angles[int(pair/10)],'dir': directions[int(pair%10)],'size': (angles[int(pair/10)])/10} 
    
    if trialInfo['dir'] == 0 and angleCalc(trialInfo['angle']) > tvInfo['rightEdge']:
        continue 
    elif trialInfo['dir'] == 2 and angleCalc(trialInfo['angle']) < tvInfo['leftEdge']:
        continue
        
    if(trialInfo['size'] == 0): # Ensure initial letter height is not 0
        trialInfo['size'] = 1
    
    # Continue to display the stimulus character and wait for subject input
    # until the staircase algorithm converges
    while not stairCaseCompleted:
        # Choose a random letter to display
        displayInfo = {'text': random.choice(letters)}
        # Calculate display coordinates for the stimulus character
        displayInfo = calculateDisplayCoords(trialInfo, displayInfo)
        # Generate a display object for the stimulus character
        displayText = genDisplay(displayInfo)
        
        # Display a blank screen with only the center dot on the first trial
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
            response = getKeyboardInput(keyL = ['e','p','b','space','escape'], loop = False, waitTime = 0.05)
            if response:
               break # Break if a keypress was detected
               
        # Check whether or not the input matched the stimulus character
        trialInfo['thisResponse'] = checkResponse(response, displayInfo['text'])
            
        # Call the staircase algorithm
        trialInfo = stairCase(trialInfo)
        
        # If the staircase has converged, output the data to the csv file
        if trialInfo['stairCaseCompleted'] and not fileName is None:
            # Write direction, threshold letter height, and retinal
            # eccentricity to csv. Direction is stored in the csv in the 
            # range of 1->4, rather than 0->3
            csvOutput([(trialInfo['dir']+1), trialInfo['size'], trialInfo['angle']], fileName) 
    
    run += 1 # Increment the number of runs completed

    # Halfway through the trial, give the subject a 30 second break and display 
    # a countdown timer on the screen
    if run == (int(len(pairs)/2)):
        expBreak()

# End the experiment after all eccentricity/direction pairs have been completed
endExp()
