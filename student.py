import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 91
    STOP_DIST = 30

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "5": ("test_drive", self.testDrive),
                "s": ("Check status", self.status),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()


    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        print("Is it clear")
        for x in range(3):
            if not self.isClear():
                print("Omgorsh, it's not safe!")
                break
            x = 175
            #while self.isClear() and x <= 200:
            print('Speed is set to:' + str(x))
            set_speed(x)
            servo(20)
            self.encB(5)
            self.encL(3)
            self.encR(4)
            self.encL(11)
            servo(90)
            self.encB(3)
            servo(110)
            self.encF(2)
            servo(30)
            servo(120)
            for x in range(5):
                self.encR(5)
            self.encL(3)
            servo(70)
            self.encL(2)
            self.encR(4)
            servo(60)
            self.encF(4)
            self.encL(2)
            for x in range(10):
                self.encF(3)
                self.encL(3)
            self.encB(6)
            self.encR(7)
            self.encL(30)
            self.encB(5)
            servo (90)
            self.encR(5)
            for x in range(5):
                self.encF(3)
                self.encB(3)
            self.encL(5)
            servo(110)
            self.encR(20)
            self.encF(6)
            servo(100)
            self.encF(5)
            servo(120)
            time.sleep(.5)
            time.sleep(.5)
            x += 25


    def status(self):
        print("My power is at "+str(volt())+ " volts")


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO: If while loop fails, check for other paths
        while True:
        ##Loop: check that it's clear -- this is MVP
            while self.isClear():
            #let's go forward just a little bit
                self.encF(5)
            ##Choose path method
            #isClear MVP
            answer = self.choosePath()
            if answer == "left":
                self.encL(3)
            elif answer == "right":
                self.encR(3)

    #Test Drive Method
    def testDrive(self):
        print("Here we go!")
        fwd()
        while True:
            if us_dist(15) < self.STOP_DIST:
                print("Ahhhhhh! All stop")
                break
            time.sleep(.05)
            print("Seems clear, keep rolling")
        self.stop()






####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()