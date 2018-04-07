
# Import Libraries
import sys
import time
import pygame
from random import randint

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.OUT)
import Adafruit_MPR121.MPR121 as MPR121
cap = MPR121.MPR121()

# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    print 'Error initializing MPR121.  Check your wiring!'
    sys.exit(1)

# initialise pygame for sounds
pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

SOUND_MAPPING = {
  0: './_sounds/c3.wav',
  1: './_sounds/d3.wav',
  2: './_sounds/e3.wav',
  3: './_sounds/f3.wav',
  4: './_sounds/g3.wav',
  5: './_sounds/a3.wav',
  6: './_sounds/b3.wav',
  7: './_sounds/c4.wav',
  8: './_sounds/d4.wav',
  9: './_sounds/d4.wav',
  10:'./_sounds/d4.wav',
  11:'./_sounds/d4.wav',
}

# setup lists
sounds = [0,0,0,0,0,0,0,0,0,0,0,0]
input = [False,False,False,False,False,False,False,False,False,False,False,False]
#song =
melody = [0,1,2,3,2,1]
melodySize = 6


#global vars
gameState = 'setup'
treeState = 'singing'
stage = 0
solved = False
tempo = 120
timeSig = 3
currentTimeBetween = 0.00
noteInterval = 2000
curNoteToListenFor = 0


# setup sounds
for key,soundfile in SOUND_MAPPING.iteritems():
        sounds[key] =  pygame.mixer.Sound(soundfile)
        sounds[key].set_volume(1);

# set last capacitive touch input
last_touched = cap.touched()

# Set the amt of audio channels
pygame.mixer.set_num_channels(256)

def CheckForInput():
    global current_touched
    global last_touched
    global pin_bit

    current_touched = cap.touched()

    # range(number to stop at) will loop a number of times.
    for i in range(12):

        #set input to False
        input[i] = False

        pin_bit = 1 << i
        if current_touched & pin_bit and not last_touched & pin_bit:
            print '{0} touched!'.format(i)
            input[i] = True

        if not current_touched & pin_bit and last_touched & pin_bit:
            #GPIO.output(17, GPIO.LOW)
            print '{0} released!'.format(i)
            input[i] = False

    last_touched = current_touched

def printAllThresholds():
    print 'Thresholds set at'
    for i in range(12):
        print '=== {0} ==='.format(i)
        print 'filtered: {0}'.format(cap.filtered_data(i))
        print 'baseline: {0}'.format(cap.baseline_data(i))

def printThreshold(pos):
    print 'filtered: {0}'.format(cap.filtered_data(pos))
    print 'baseline: {0}'.format(cap.baseline_data(pos))

def SetNewMelody():

    global melody
    for i in range(melodySize):

        melody[i] = randint(0,5)

def CorrectInputFeedback():
    print('correct input fb {0}').format(curNoteToListenFor)

def GameWon()
    global gameState 
    gameState = "finish"
    pass

def StageComplete():
    global curNoteToListenFor
    global stage
    curNoteToListenFor = 0
    if stage == finalStage:
        GameWon()
    else: 
        stage = stage + 1
        time.sleep(2)
        SingMelody(stage+1)

def SingMelody(singToThisNote):
    for i in range(singToThisNote):
        sounds[melody[i]].play()
        time.sleep(0.4)

def CompareInputToMelody():
    global curNoteToListenFor

    if input[melody[curNoteToListenFor]] == True:
        curNoteToListenFor = curNoteToListenFor + 1
        if curNoteToListenFor >= (stage + 1):
            StageComplete()
        else:
            CorrectInputFeedback()

def PingWebpage():
    subprocess.call("curl https://www.gold.ac.uk", shell=True)

# main loop
while True:
    if gameState == 'setup':

        #Setup vars
        solved = False
        currentNote = 1
        currentTimeBetween = 0.0
        #touch, release
        cap.set_thresholds(20,10)
        print 'Press Ctrl-C to quit'

        SetNewMelody()
        SingMelody(1)
        # go to next state
        gameState = 'live'
        treeState = 'listening'

    elif gameState == 'live':

        CheckForInput()

        # play sounds if true
        for i in range(12):
            if input[i] == True:
                sounds[i].play()

        elif treeState == 'listening':
            # listening Treestate
            print('current note: {0} | stage: {1} | note needed {2}').format(curNoteToListenFor,stage,melody[curNoteToListenFor])
            CompareInputToMelody()

    elif gameState == 'finish':
        printGState()
        PingWebpage()
        gameState = 'end'

    elif gameState == 'end':
        pass
