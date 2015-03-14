#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import random
import tweepy

consumer_key = "x"
consumer_secret = "x"

#using basic OAUTH2
access_token = "x"
access_token_secret = "x"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

activated = True

compList = ["Hope you're having a wonderful day!"  ,
            "Remember, you're beautiful!"          ,
            "Don't let anybody push you around!"   ,
            "Carpe diem! Seize the day!"         ]


def removeTweets(num):
        """

        Accepts a parameter of # of tweets wanted to remove.
        Removes in reverse-Chronological order.

        """
        timeline = api.user_timeline(count = num)

        if (len(timeline)) == 0:
                print("None found!")
        else:
                print "Found: %d" % (len(timeline))
                for t in timeline:
                        api.destroy_status(t.id)
        return


def getRandomCompliment():
        """

        Grabs a random compliment from the global[] compList.
        Sends a non-duplicate tweet.

        """
        global compList
        randomCompliment = compList[random.randrange(0, len(compList))]

        try: # send the random compliment
                sendTweet(randomCompliment)
        except tweepy.error.TweepError: # prevents crashing
                print('Invalid or duplicate Tweet! Try again!')


def getCurrentStatus():
        for status in tweepy.Cursor(api.user_timeline).items():
                id = status.id
                currStatus = api.get_status(id).text
                return(currStatus)

def regulateLEDS(*args):
        #initalize all of the LEDs
        for unpack in args:
                for indvLED in unpack:
                        #set all to off
                        GPIO.output(indvLED, GPIO.LOW)
                        return('success!')
        #issue flag raised
        return('config failed')


def initBoard():
        #initialize preferable board settings
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        #initialize individual pins
        buttonPins = [ 3 , 5 ]
        ledPins =    [ 7 , 13 ]

        for individualPin in buttonPins:
                GPIO.setup(individualPin, GPIO.IN)

        for individualPin in ledPins:
                GPIO.setup(individualPin, GPIO.OUT)

        print(regulateLEDS(ledPins))
        inputHandler(buttonPins[0],
                     buttonPins[1])


def blinkIndicator(indID, freqMult, leng):
        tempTimer = 0

        while tempTimer < leng:
                GPIO.output(indID, GPIO.HIGH)
                time.sleep(freqMult)
                GPIO.output(indID, GPIO.LOW)
                time.sleep(freqMult)
                tempTimer+=1

        return('done')


def sendTweet(compliment):
        global api

        print('Updating status. . . . .')
        api.update_status(compliment)

        print('. . . . . Status updated to: %s.' % compliment)
        blinkIndicator(13, 1, 1)


def inputHandler(data1, data2):
        global activated
        global compList

        while activated:
                print('awaiting input ... ')
                if GPIO.input(data1) == 0:
                        getRandomCompliment()
                time.sleep(1.5)


initBoard()
GPIO.cleanup()
