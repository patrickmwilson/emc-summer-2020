
from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.hardware import keyboard
import os, time, csv, random

# Opens the csvFile and writes the output argument specified by to the file
def csvOutput(output, fileName):
    with open(fileName,'a', newline ='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()
    
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
fileName = os.path.join(os.getcwd(), 'reaction_time_data.csv')

csvOutput(['Number of Characters', 'Reaction Time (ms)'], fileName)

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(200)
win = visual.Window( size=(1920, 1080), fullscr=True, screen=0, winType='pyglet', allowGUI=True,
    monitor= mon, color='grey', blendMode='avg', useFBO=True, units='cm')
    
displayText = visual.TextStim(win=win, text= "", font='Arial', pos=(0, 0), height=5, color='white')
    
    
possible = ["I", "II", "III"]

for i in range(10):
    
    displayText.text = ""
    displayText.draw()
    win.flip()
    time.sleep(random.randint(1,5))
    
    stim = random.choice(possible)
    
    if stim == "I":
        correctAnswer = 1
        correctKey = '1'
    elif stim == "II":
        correctAnswer = 2
        correctKey = '2'
    else:
        correctAnswer = 3
        correctKey = '3'
        
    displayText.text = stim
    displayText.draw()
    
    times = {'start': 0, 'end': 0}

    win.timeOnFlip(times, 'start')

    win.flip()

    keys = event.waitKeys(timeStamped=True, keyList = [correctKey, 'escape'])
    
    key = keys[0]
    
    if key[0] == 'escape':
        core.quit()

    times['end'] = key[1]
    
    reactionTime = times['end'] - times['start']
    
    csvOutput([correctAnswer, reactionTime], fileName)

core.quit() 