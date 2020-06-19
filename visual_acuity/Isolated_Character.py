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
from calibration import *

calibrated = checkCalibration()
while not calibrated:
    calibrate()
    calibrated = checkCalibration()

# Experimental variables
letters = list("EPB") # Possible stimulus characters to be displayed
keys = ['e', 'p', 'b', 'space'] # Keypresses to listen for 
angles = [0, 5, 10, 15, 20, 25, 30, 35, 40] # Retinal eccentricity (opening angle) values to test
directions = [0, 2] # 0 = Right (0°), 2 = Left (180°)
distToScreen = 50 # Distance between the subject and the screen in centimeters
trials = 1 # Number of trails to run
green= [.207, 1, .259] # Defining green color for center dot

# End the experiment: close the window, flush the log, and quit the script
def endExp():
    win.flip()
    logging.flush()
    win.close()
    core.quit()

# Input dialogue: record data to csv file? If yes, create the csv file for data output
fileName = createOutputFile('Isolated Character')

# Create a window for stimulus display, as well as a keyboard object for subject input
win, keyPress = createPsychopyObjects()

# Display experiment instructions, end the experiment if the subject presses the esc key
dispInfo = {'text': '    Press the key corresponding to the character \n         displayed in the periphery, or space bar \n                        if you can not read it    \n\n                 Press spacebar to continue',\
    'xPos': 0, 'yPos': 5, 'heightCm': 5, 'color': 'white', 'win': win}
if not instructions(dispInfo):
    endExp()
dispInfo = {'text': '  Take some time to familiarize yourself with the keys\n\n                       Press spacebar to begin',\
    'xPos': 0, 'yPos': 0, 'heightCm': 5, 'color': 'white', 'win': win}
if not instructions(dispInfo):
    endExp()

# Generate display object for the green dot in the center of the screen
dot = genDot(win, green)

# Generate a list of angle and direction pairs to test
pairs = genPairs(angles, directions)
run = 0 # Store the number of trials completed
for pair in pairs: # Loop through the list of pairs
    
    # Initialize trial variables related to staircase algorithm
    trialInfo = {'numReversals': 0, 'totalReversals': 0, 'responses': 0,\
        'thisResponse': False, 'lastResponse': False, 'stairCaseCompleted': False,\
        'angle': angles[int(pair/10)],'dir': directions[int(pair%10)],'size': (angles[int(pair/10)])/10} 
        
    if(trialInfo['size'] == 0): # Ensure initial letter height is not 0
        trialInfo['size'] = 1
    
    # Continue to display the stimulus character and wait for subject input
    # until the staircase algorithm converges
    while not stairCaseCompleted:
        
        # Choose a random letter to display
        displayInfo['text'] = random.choice(letters)
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
            
            # Clear the keyboard input buffer upon screen flip
            win.callOnFlip(keyPress.clearEvents, eventType='keyboard')
            win.flip() # Update the display
            
            # Pause execution for 0.05 seconds and listen for keypress
            response = event.waitKeys(maxWait = 0.05, keyList = keys, clearEvents = False)
            
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
