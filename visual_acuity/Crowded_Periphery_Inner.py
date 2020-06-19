# Crowded Periphery Inner
#
# Displays 5 characters arranged in a plus ('+') in the peripheral region. The 
# subject is tasked with identifying the character on the inside of the plus.
# To see a photo of this experiment, open the 'cp.png' file within the 
# 'Protocol Pictures' folder
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
import os, sys, time, random, math, csv, serial

# Create a serial object to read subject input from the arduino controlling the
# push buttons. Change the port parameter to the port your arduino is
# connected to.
ser = serial.Serial(port='COM3', baudrate=9600, parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=None)

# Opens the csvFile and writes the output argument specified by to the file
def csvOutput(output):
    with open(fileName, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()

# End the experiment: close the window, flush the log, and quit the script
def endExp():
    win.flip()
    logging.flush()
    win.close()
    core.quit()


# Input dialogue: record data to csv file?
datadlg = gui.Dlg(title='Record Data?', pos=None, size=None, style=None,
                  labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
ok_data = datadlg.show()
recordData = datadlg.OK


# Create a csv file for data output and the folder to store it in
if recordData:
    # Change directory to script directory
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    # Store info about experiment, get date
    expName = 'Crowded Periphery Inner'
    date = time.strftime("%m_%d")
    expInfo = {'Session Type': '', 'Subject Code': ''}

    # Input dialogue: session type, subject code
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()

    # Create folder for data file output (cwd/Analysis/Data/<type>/<subject code>)
    OUTPATH = os.path.join(os.getcwd(), 'Analysis', 'Data',
                           expInfo['Session Type'], expInfo['Subject Code'])
    os.mkdir(OUTPATH)

    # Output file name: <OUTPATH>/<subject code_data_expName.csv>
    fileName = os.path.join(OUTPATH, (expInfo['Subject Code'] + '_' + date +
                                      '_' + expName + '.csv'))

    # Print column headers if the output file does not exist
    if not os.path.isfile(fileName):
        csvOutput(["Direction", "Letter Height (degrees)",
                   "Eccentricity (degrees)"])

# Input dialogue: test horizontal angles only?
datadlg = gui.Dlg(title='Horizontal angles only?', pos=None, size=None,
                  style=None, labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
ok_data = datadlg.show()
horizontalOnly = datadlg.OK

# Create visual window - monitor setup is required beforehand, can be found in
# psychopy monitor tab. Set window size to the resolution of your display monitor
mon = monitors.Monitor('TV')  # Change this to the name of your display monitor
mon.setWidth(200)
win = visual.Window(
    size=(3840, 2160), fullscr=False, screen=-1,
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor=mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='cm')

# Experimental variables
letters = list("EPB")  # Possible stimulus characters to be displayed
# Horizontal retinal eccentricity (opening angle) values to test
anglesH = [5, 10, 15, 20, 25, 30, 35, 40]
# Vertical retinal eccentricity (opening angle) values to test
anglesV = [5, 10, 15, 20, 25, 30]
# Horizontal directions: 0 = Right (0°), 2 = Left (180°)
directionsH = [0, 2]
# Vertical directions: 1 = Down (270°), 3 = Up (90°)
directionsV = [1, 3]
# Distance between the subject and the screen in centimeters
distToScreen = 50
# Number of trails to run
trials = 1
# Defining green color for center dot
green = [.207, 1, .259]

# Spacing adjustments for text display - These are unique to the particular
# monitor that was used in the experiment and would need to be modified
# manually for correct stimulus display
dirXMult = [1.62, 0, -1.68, 0]  # Multiply x position by this value
dirYMult = [0, -1.562, 0, 1.748]  # Multiply y position by this value
yOffset = [0.2, 0, 0.2, 0]  # Offset y position by this value

# Returns a displayText object with the given text, coordinates, height, color
def genDisplay(text, xPos, yPos, height, colour):
    displayText = visual.TextStim(win=win,
    text= text,
    font='Arial',
    pos=(xPos, yPos), height=height, wrapWidth=500, ori=0, 
    color=colour, colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0)
    return displayText

# Staircase algorithm which determines when to end a trial (identifies the
# threshold identifiable letter height)
def stairCase(thisResponse, numReversals, totalReversals, size, stairCaseCompleted, lastResponse, responses):
    # Increment the number of responses recorded from the subject
    responses += 1
    
    # Reset numReversals if there are two sequential correct or incorrect
    # answers. Update the number of total reversals
    if numReversals > 0 and lastResponse == thisResponse:
        totalReversals += numReversals
        numReversals = 0
    
    # If the subject correctly identified the stimulus character, decrease the
    # size of the stimulus character
    if thisResponse:
        if numReversals == 0 and size > 1:
            # Decrease display size rapidly until an incorrect identification is
            # made (while the size is > 1°)
            size -= 0.5
        elif(size > 0.5):
            # Reduce the display size change decrement to 0.2 if the
            # size is < 0.5°
            size -= 0.2
        else:
            # Once a reversal has been made (after the first incorrect
            # identification), decrease size by 0.1°
            size -= 0.1
    # If the subject incorrectly identified the stimulus character, increase the
    # size of the stimulus character
    else:
        # Once a reversal has been made (after the first incorrect
        # identification), decrease size by 0.1°
        numReversals += 1
        if size > 0.5:
            size += 0.2
        else:
            size += 0.1
            
    # Staircase algorithm convergence. Conditions for convergance: 3 or more
    # consecutive reversals, 15 or more total reversals, 25 or more responses.
    # If one of these conditions is met, the staircase converges and returns
    # true. The letter height of the last correctly identified stimulus
    # character is recorded as the threshold letter height
    if numReversals >= 3 or responses >= 25 or totalReversals > 15:
        stairCaseCompleted = True

    # If the display size has been lowered to > 0.1°, set it to 0.1°, because
    # the monitor used in our experiment was unable to clearly display
    # characters smaller than that size
    if size < 0.1:
        size = 0.1
        
    return stairCaseCompleted, size, numReversals, totalReversals,\
         thisResponse, responses

# Takes a value in the form of angle of visual opening and returns the
# equivalent value in centimeters (based upon the distToScreen variable)
def angleCalc(angle):
    radians = math.radians(angle)  # Convert angle to radians
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
def displayVariables(angle, dir, size):
    spacingAdjustment = 2.3378
    # Stimulus height in cm
    heightCm = (angleCalc(size)*spacingAdjustment)
    # Stimulus distance from the screen's center in cm
    angleCm = angleCalc(angle)
    # Stimulus display x position
    xPos = (dirXMult[dir]*angleCm)
    # Stimulus display y position
    yPos = (dirYMult[dir]*angleCm) + yOffset[dir]
    
    if angle == 0 and dir %2 != 0: # TODO: TEST THE CODE WITHOUT THIS LINE. MAY BE UNNECESSARY
        yPos += 0.2
    return heightCm, angleCm, xPos, yPos

# Generates and displays a plus ('+') pattern of 5 characters randomly selected
# from 'E', 'B', and 'P'. Returns the target character (the inner character of 
# the plus pattern, closest to the center of the screen)
#
#  P
# EEB
#  B
#
def genArray(size, heightCm, xPos, yPos, direction):
    # Spacing adjustment for distance between the rows of characters
    spacer = (size*1.4)*1.1
    
    rows = 3
    colsPerRow = [1, 3, 1]
    
    # Set the index of the inner character in the plus pattern based upon the 
    # direction relative to the center of the screen in which it is displayed
    if direction == 0:
        innerRow = 1
        innerCol = 0
    elif direction == 1:
        innerRow = 0
        innerCol = 0
    elif direction == 2:
        innerRow = 1
        innerCol = 2
    elif direction == 3:
        innerRow = 2
        innerCol = 0

    # Fill and display each row
    for i in range(rows):
        # Set vertical position of the row based on its index
        yCoord = yPos + (spacer*(1 - i))
        
        # List to store characters in the line
        line = list(range(0))

        cols = colsPerRow[i]
        for j in range(cols):
            # Choose a random letter from E, B, and P
            char = random.choice(letters)
            # Append the character to the line list
            line.append(char)
            
            # Return the inner character, as the subject will be tasked with 
            # identifying it
            if(i == innerRow and j == innerCol):
                innerChar = char
        
        # Convert the list to a string, create a display object, and draw it
        line = ''.join(line)
        lineDisplay = genDisplay(line, xPos, yCoord, heightCm, 'white')
        lineDisplay.draw()
    return innerChar

# Returns a boolean indicating whether or not the subject's input matched the
# stimulus character
def checkResponse(button, letter):
    key = '0'
    if button == 1:
        key = 'e'
    elif button == 2:
        key = 'b'
    elif button == 3:
        key = 'p'
    elif button == 4:  # Do not know/cannot guess button
        key = 'space'
    return (key == letter.lower())


# Display on-screen instructions
instructions = genDisplay('    Press the button corresponding to the character \n         at the inside of the pattern, closest to the green dot \n         or the black button if you can not read it    \n\n                 Press Any Button to continue', 0, 5, 5, 'white')
instructions.draw()
win.flip()
while(1):  # Wait until the subject presses a button
    if ser.in_waiting:
        a = ser.readline()  # Read in the input value to clear the buffer
        break
    else:
        time.sleep(0.05)
    
# Display on-screen instructions
instructionText = '  Take some time to familiarize yourself with the buttons\n\n                       Press any button to begin'
instructions = genDisplay(instructionText, 0, 0, 5, 'white')
instructions.draw()
win.flip()
while(1):  # Wait until the subject presses a button
    if ser.in_waiting:
        a = ser.readline()  # Read in the input value to clear the buffer
        break
    else:
        time.sleep(0.05)
    

# Generate display object for the green dot in the center of the screen
dot = genDisplay('.', 0, 1.1, 4, green)

# Generate a randomized list of angle and direction pairs. Each pair is
# represented as a single integer. The index of the angle (in the angles array)
# is multiplied by 10, and the index of the direction (in the directions array)
# is added to it. Positive values represent horizontal pairs, and negative
# represent vertical.
pairs = list(range(0))
for i in range(trials):
    for j in range(len(anglesH)):  # Loop through horizontal angles
        for k in range(len(directionsH)):  # Loop through horizontal directions
            pairs.append((j*10)+k)
    if not horizontalOnly:
        for l in range(len(anglesV)):
            for m in range(len(directionsV)):
                pairs.append(-((l*10)+m))
shuffle(pairs)  # Randomize the pairs list

run = 0  # Store the number of trials completed
for pair in pairs:  # Loop through the list of pairs
    if(pair >= 0):  # Horizontal pairs
        angle = anglesH[int(pair/10)]  # Angle index = pair/10
        dir = directionsH[(pair % 10)]  # Direction index = pair%10
    else:  # Vertical pairs
        angle = anglesV[abs(int(pair/10))]  # Angle index = pair/10
        dir = directionsV[abs(pair % 10)]  # Direction index = pair%10
        
    size = angle/10  # Set initial letter height
    if(size == 0):  # Ensure initial letter height is not 0
        size = 1

    # Initialize trial variables related to staircase algorithm
    numReversals, totalReversals, responses = 0, 0, 0
    lastResponse, stairCaseCompleted = False, False
    
    # Continue to display the stimulus character and wait for subject input
    # until the staircase algorithm converges
    while not stairCaseCompleted:
        # Clear the graphics buffer
        win.clearBuffer()
            
        # Display a blank screen with only the center dot on the first trial
        if responses == 0 and run == 0:
            dot.draw()
            win.flip()
            
        time.sleep(0.5)

        # Calculate display coordinates for the stimulus
        heightCm, angleCm, xPos, yPos = displayVariables(angle, dir, size)

        # Generate and display a new randomized plus pattern of stimulus
        # characters, return the inner character of the pattern
        innerChar = genArray(size, heightCm, xPos, yPos, dir)
        
        # Display the center green dot. Every 0.05 seconds, hide/display the dot
        # to create a flashing effect
        flash = False
        while 1:
            flash = (flash == False)
            if flash:
                # Generate a display object for the green dot
                dot = genDisplay('.', 0, 1.1, 4, green)
            else:
                # Generate a display object to hide the dot
                dot = genDisplay('.', 0, 1.1, 4, 'grey')
            
            # Display the dot
            dot.draw()

            # Refresh the display without clearing the buffer, to preserve the
            # display of the stimulus characters
            win.flip(clearBuffer = False)
            if ser.in_waiting:
                # Read the serial input buffer
                value = float(ser.readline().strip())
                # Convert input to int
                button = int(value)
                break
            else:
                time.sleep(0.05)
        
        # Check whether or not the input matched the target character
        thisResponse = checkResponse(button, innerChar)
            
        # Call the staircase algorithm
        stairCaseCompleted, size, numReversals, totalReversals, lastResponse,\
             responses = stairCase(thisResponse, numReversals, totalReversals,\
                  size, stairCaseCompleted, lastResponse, responses)
        
        # If the staircase has converged, output the data to the csv file
        if stairCaseCompleted:
            # Direction is stored in csv in the range of 1->4, rather than 0->3
            direction = dir+1
            if recordData:
                # Write direction, threshold letter height, and retinal
                # eccentricity to csv
                csvOutput([direction, size, angle])
                    
    # Increment the number of runs completed
    run += 1

    # Halfway through the trial, give the subject a 30 second break and display
    # a countdown timer on the screen
    if run == (int(len(pairs)/2)):
        for i in range(30):
            win.clearBuffer()
            seconds = str(30-i)
            breakText = genDisplay('Break', 0, 0, 5, 'white')
            secondText = genDisplay('Seconds', +2, -5, 5, 'white')
            numText = genDisplay(seconds, -11, -5, 5, 'white')
            breakText.draw()
            secondText.draw()
            numText.draw()
            win.flip()
            time.sleep(1)

# End the experiment
endExp()
