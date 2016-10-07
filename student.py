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
    STOP_DIST = 20

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
        x = 100
        while self.isClear() and x <= 200:
            print('Speed is set to:' + str(x))
            set_speed(x)
            servo(20)
            self.encB(5)
            self.encL(3)
            self.encR(50)
            self.encL(11)
            servo(90)
            self.encB(3)
            servo(110)
            self.encF(2)
            servo(30)
            self.encR(5)
            self.encR(5)
            self.encR(5)
            self.encR(5)
            self.encR(5)
            self.encL(3)
            servo(70)
            self.encL(2)
            self.encR(4)
            servo(60)
            self.encF(4)
            self.encL(2)
            self.encB(6)
            self.encR(7)
            self.encL(30)
            self.encB(5)
            servo (90)
            self.encR(5)
            self.encB(3)
            servo (110)
            self.encR(20)
            self.encF(6)
            servo(100)
            self.encF(5)
            servo(120)
            time.sleep(.5)


    def status(self):
        print("My power is at "+str(volt())+ " volts")


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE


####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()