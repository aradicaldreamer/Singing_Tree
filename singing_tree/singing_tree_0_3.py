
# Import Libraries
import sys
import time
import pygame
import subprocess
import webbrowser
from random import randint


import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
p = GPIO.PWM(19,100)
p.start(0)

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
  0: './_sounds/OGG/C2.ogg',
  1: './_sounds/OGG/D2.ogg',
  2: './_sounds/OGG/Eb2.ogg',
  3: './_sounds/OGG/F2.ogg',
  4: './_sounds/OGG/G2.ogg',
  5: './_sounds/OGG/A2.ogg',
  6: './_sounds/OGG/Bb2.ogg',
  7: './_sounds/OGG/C3.ogg',
  8: './_sounds/OGG/D3.ogg',
  9: './_sounds/OGG/Eb3.ogg',
  10:'./_sounds/OGG/F3.ogg',
  11:'./_sounds/OGG/G3.ogg',
  12:'./_sounds/OGG/A3.ogg',
  13:'./_sounds/OGG/Bb3.ogg',
  14:'./_sounds/OGG/C4.ogg',
}

# setup lists
sounds = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
input = [False,False,False,False,False,False,False,False,False,False,False,False]
#song =
melody = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
melodySize = 4


#global vars
gameState = 'setup'
treeState = 'singing'
stage = 0
solved = False
lastStage = 4

curNoteToListenFor = 0
inputRecieved = False
melodyReplay = 0
melodyReplayThreshold = 5
replayCount = 0
replaysUntilReset = 5
melodyLastPlayed = time.time()


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
    global replayCount

    current_touched = cap.touched()

    # range(number to stop at) will loop a number of times.
    for i in range(12):

        #set input to False
        input[i] = False

        pin_bit = 1 << i
        if current_touched & pin_bit and not last_touched & pin_bit:
            print '{0} touched!'.format(i)
##            GPIO.output(17, GPIO.HIGH)
            input[i] = True

        if not current_touched & pin_bit and last_touched & pin_bit:
##            GPIO.output(17, GPIO.LOW)
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

        melody[i] = randint(0,8)

def CorrectInputFeedback():
    print('correct input fb {0}').format(curNoteToListenFor)

def GameWon():
    global gameState
    gameState = 'finish'

def StageComplete():
    global curNoteToListenFor
    global stage
    global melodyReplayThreshold 
    
    if stage == (melodySize - 1):
        GameWon()
    else:
        curNoteToListenFor = 0
        stage = stage + 1
        melodyReplayThreshold = 3 + stage
        pygame.mixer.fadeout(2000)
        time.sleep(2)
        SingMelody(stage+1)

def ResetMelodyLastPlayed():
    global melodyLastPlayed
    global melodyReplay
    melodyLastPlayed = time.time()
    melodyReplay = 0
    

def SingMelody(singToThisNote):
    ResetMelodyLastPlayed()
    for i in range(singToThisNote):
        sounds[melody[i]].play()
        time.sleep(0.4)

def IncorrectNoteFeedback():
    time.sleep(0.5)
    sounds[1].play()
    sounds[3].play()
    sounds[5].play()
    sounds[6].play()
    time.sleep(0.5)

def CompareInputToMelody():
    global curNoteToListenFor

    if input[melody[curNoteToListenFor]] == True:
        curNoteToListenFor = curNoteToListenFor + 1
        if curNoteToListenFor >= (stage + 1):
            StageComplete()
        else:
            CorrectInputFeedback()
    elif input[melody[curNoteToListenFor]] == False:
        if inputRecieved == True:
            curNoteToListenFor = 0
##            IncorrectNoteFeedback()

def PingWebpage():
    subprocess.call("curl https://www.gold.ac.uk", shell=True)


# main loop
while True:
    if gameState == 'setup':

        #Setup vars
        solved = False
        stage = 0
        currentNote = 1
        currentTimeBetween = 0.0
        melodyReplayThreshold = 3
        replayCount = 0
        #touch, release
        cap.set_thresholds(20,10)
        print 'Press Ctrl-C to quit'

##
##        while True:
##            for x in range(75):
##                p.ChangeDutyCycle(x)
##                print(x)
##                time.sleep(0.001)
##
##            for x in range(75):
##                p.ChangeDutyCycle(75-x)
##                print(x)
##                time.sleep(0.001)

        SetNewMelody()
        SingMelody(1)
        # go to next state
##        webbrowser.open('http://www.google.com',1)
        subprocess.call("curl https://www.gold.ac.uk", shell=True)
##        p.kill()
##        webbrowser.open("http://www.google.com")
##        subprocess.Popen(["chromium-browser"])
        print('webpage opened')
        gameState = 'live'
        treeState = 'listening'

    elif gameState == 'live':

        CheckForInput()
        
        if replayCount >= replaysUntilReset:
            gameState = 'setup'
            time.sleep(4)
        
        
        melodyReplay = time.time() - melodyLastPlayed
        if melodyReplay >= melodyReplayThreshold:
            SingMelody(stage+1)
            replayCount = replayCount + 1


        # play sounds if true
        for i in range(12):
            if input[i] == True:
                sounds[i].play()
                inputRecieved = True
                replayCount = 0

        # === Tree State Switch ===
        if treeState == 'singing':
            # singing Treestate
            if stage == 0:
                SingMelody()


        elif treeState == 'listening':
            # listening Treestate
            print('notePos: {0} | stage: {1} | note {2} | replay {3} | untilReset {5}/{4}').format(curNoteToListenFor,stage,melody[curNoteToListenFor],melodyReplay,replaysUntilReset,replayCount)
            CompareInputToMelody()
        # === Tree State Switch ===
        # check if an input was pressed this loop. if true reset melody timeout.
        if inputRecieved == True:
            ResetMelodyLastPlayed()
        # reset input recieved
        inputRecieved = False

    elif gameState == 'finish':
##        PingWebpage()
        gameState = 'end'
        
    elif gameState == 'end':
        for i in range(12):
            sounds[i].play()
            time.sleep(0.150)
        sounds[0].play()
        time.sleep(0.025)
        sounds[2].play()
        time.sleep(0.025)
        sounds[4].play()
        time.sleep(0.025)
        sounds[6].play()
        time.sleep(2)
        sounds[8].play()
        time.sleep(0.1)
        sounds[8].play()
        time.sleep(5)
        print('end')
        gameState = 'perform'

    elif gameState == 'perform':
        for i in range(2):
            for i in range(melodySize):
                sounds[melody[i]].play()
                time.sleep(0.4)
            time.sleep(1.2)
        gameState = 'end-game'
        
    elif gameState == 'end-game':
        time.sleep(10)
	gameState = 'setup'
        

