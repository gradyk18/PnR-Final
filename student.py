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
    RIGHT_SPEED = 169
    LEFT_SPEED = 172
    speed = 100
    scan = [None] * 180

    turn_track = 0.0
    TIME_PER_DEGREE = 0.0058
    TURN_MODIFIER = .75

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
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

    #added setSpeed to my code
    def setSpeed(self, left, right):
        set_left_speed(left)
        set_right_speed(right)
        self.LEFT_SPEED = left
        self.RIGHT_SPEED = right
        print('Left speed set to: ' + str(left) + ' // Right set to: ' + str(right))

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

    # my new time method

    ##def turnR(self, deg):
        # TWO NEW DISTANCE VARIABLES ARE NEEDED:
        # 1) TIME_PER_DEGREE - the answer to today's email
        # 20 TURN_MODIFIER - the change to the speed you used
       # print("Let's turn" + str(deg) + "degrees right")
       # print("That means I turn for" + str(deg * self.TIME_PER_DEGREE) + "seconds")

        #print("Let's change our motor speeds!")
       # set_left_speed(int(self.LEFT_SPEED * self.TURN_MODIFIER))
       # set_right_speed(int(self.RIGHT_SPEED * self.TURN_MODIFIER))

       # right_rot()
        #time.sleep(deg * self.TIME_PER_DEGREE)
       # self.stop()

        # Let's turn the speed back to normal
       # set_left_speed(self.LEFT_SPEED)
        #set_right_speed(self.RIGHT_SPEED)

    ############################
    ##MY NEW TURN METHODS because encR and encL just don't cut it
    ############################
    #takes number of degrees and turns right accordingly
    def turnR(self, deg):
        #blah
        self.turn_track += deg
        print("The exit is" + str(self.turn_track) + "degrees away.")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop())
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)


    def turnL(self, deg):
        #adjust the tracker so we know how many degrees away our exit is
        self.turn_track -= deg
        print("The exit is" + str(self.turn_track) + "degrees away.")
        self.setSpeed(self.LEFT_SPEED * self.TURN_MODIFIER,
                      self.RIGHT_SPEED * self.TURN_MODIFIER)
        #do turn stuff
        left_rot()
        #use our experiment to calculate the time needed to turn
        time.sleep(deg * self.TIME_PER_DEGREE)
        self.stop()
        #return speed to normal
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)



    def setSpeed(self, left, right):
        print("Left speed:" + str(left))
        print("Right speed:" + str(right))
        set_left_speed(left)
        set_right_speed(right)
        time.sleep(.05)


    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #TODO: If while loop fails, check for other paths
        while True:
        ##Loop: check that it's clear -- this is MVP
            while self.isClear():
            #let's go forward just a little bit
            #added test drive into nav
                self.testDrive()
            ##Choose path method
            #isClear MVP
            #now using turnL and turnR instead of enc
            answer = self.choosePath()
            if answer == "left":
                self.turnL(45)
            elif answer == "right":
                self.turnR(45)






    # Test Drive Method
    def testDrive(self):
        #add code so servo faces forward
        servo(self.MIDPOINT)
        time.sleep(.1)
        print("Here we go!")
        fwd()
        #loop-- will continue until something gets in the way
        while True:
            if us_dist(15) < self.STOP_DIST:
                print("Ahhhhhh! All stop")
                break
            time.sleep(.05)
            print("Seems clear, keep rolling")
        self.stop()

#calibrate robot
    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        response = input("Do you want to check if I'm driving straight? (y/n)")
        if response == 'y':

            while True:
                set_left_speed(self.LEFT_SPEED)
                set_right_speed(self.RIGHT_SPEED)
                print("Left: " + str(self.LEFT_SPEED) + "//  Right: " + str(self.RIGHT_SPEED))
                self.encF(9)
                response = input("Reduce left, reduce right or done? (l/r/d): ")
                if response == 'l':
                    self.LEFT_SPEED -= 10
                elif response == 'r':
                    self.RIGHT_SPEED -= 10
                else:
                    break

#TODO: make sure the robot does not turn backward during the maze by using Mr. A's strategy
#Add code from Mr. A's video






####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')



def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()