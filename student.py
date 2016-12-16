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
    # These are used throughout the code
    MIDPOINT = 91
    STOP_DIST = 20
    RIGHT_SPEED = 169
    LEFT_SPEED = 172
    scan = [None] * 180

    turn_track = 0
    TIME_PER_DEGREE = 0.0058
    TURN_MODIFIER = .75

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        #self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        #left needs to be before right speed
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        #added things to the menu
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "5": ("test_drive", self.testDrive),
                "6": ("test turn", self.testTurn),
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
    #First project we did with the robot
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


    ############################
    ##MY NEW TURN METHODS because encR and encL just don't cut it ~ more advanced
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
        self.stop()
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
        set_left_speed(int(left))
        set_right_speed(int(right))
        time.sleep(.05)


    # AUTONOMOUS DRIVING - central logic loop of my navigation
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #main app loop
        while True:
        #ADD THIS LOOP
        #this will make it so it doesn't keep scanning
        #for x in range(3):
        #not as good as other option
        ##Loop: check that it's clear -- this is MVP
            if self.isClear():
                #let's go forward just a little bit
                #added test drive into nav
                self.testDrive()
                print("lets go!!")
            ##Choose path method
            #isClear MVP
            #answer = self.choosePath()

            #this is where backup method is in my code
            self.backUp()
            #IF I HAD TO STOP, PICK A BETTER PATH
            #new and improved method called kenny
            turn_target = self.kenny()
            #a positive turn is right
            if turn_target > 0:
                self.turnR(turn_target)
            #negative degrees means left
            #negative degrees means left
            else:
                #remove the negative with abs()
                self.turnL(abs(turn_target))






                #################################

        ### THE KENNY METHOD OF SCANNING - experimental

    def kenny(self):
        # Activate our scanner!
        self.wideScan()
        # count will keep track of continuous positive readings
        count = 0
        # list of all the open paths we detect
        option = [0]
        # YOU DECIDE: What do we add to STOP_DIST when looking for a path fwd?
        SAFETY_BUFFER = 30
        # YOU DECIDE: what increment do you have your wideScan set to?
        INC = 2

        ###########################
        ######### BUILD THE OPTIONS
        # loop from the 60 deg right of our middle to 60 deg left of our middle
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60):
            # ignore all blank spots in the list
            if self.scan[x]:
                # add 30 if you want, this is an extra safety buffer
                if self.scan[x] > (self.STOP_DIST + SAFETY_BUFFER):
                    count += 1
                # if this reading isn't safe...
                else:
                    print("This path won't work")
                    # aww nuts, I have to reset the count, this path won't work
                    count = 0
                # YOU DECIDE: Is 16 degrees the right size to consider as a safe window?
                if count > (16 / INC) - 1:
                    # SUCCESS! I've found enough positive readings in a row
                    print("---FOUND OPTION: from " + str(x - 16) + " to " + str(x))
                    # set the counter up again for next time
                    count = 0
                    # add this option to the list
                    option.append(x - 8)

        ####################################
        ############## PICK FROM THE OPTIONS - experimental

        # The biggest angle away from our midpoint we could possibly see is 90
        bestoption = 90
        # the turn it would take to get us aimed back toward the exit - experimental
        ideal = -self.turn_track
        print("\nTHINKING. Ideal turn: " + str(ideal) + " degrees\n")
        # x will iterate through all the angles of our path options
        for x in option:
            # skip our filler option
            if x != 0:
                # the change to the midpoint needed to aim at this path
                turn = self.MIDPOINT - x
                # state our logic so debugging is easier
                print("\nPATH @  " + str(x) + " degrees means a turn of " + str(turn))
                # if this option is closer to our ideal than our current best option...
                if abs(ideal - bestoption) > abs(ideal - turn):
                    # store this turn as the best option
                    bestoption = turn
        if bestoption > 0:
            print("\nABOUT TO TURN RIGHT BY: " + str(bestoption) + " degrees")
        else:
            print("\nABOUT TO TURN LEFT BY: " + str(abs(bestoption)) + " degrees")
        return bestoption

    #added wideScan method which we are using in the kenny method
    # SEARCH 120 DEGREES COUNTING BY 2's
    #this scans further to each side so the robot hopefully won't clip the side of a box
    def wideScan(self):
        # dump all values
        self.flushScan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +2):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            #absolute value because number cannot be negative
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            time.sleep(.01)

    #Test Turn Method
    #this method is for me to check and see that my robot is making accurate turns
    def testTurn(self):
        print('Lets see if our tracking is accurate')
        self.turnR(50)
        self.turnL(60)
        input('Am I about 10 degrees away from my starting direction?')
        self.turnL(80)
        input('Am I 90 degrees from the start?')


    # Test Drive Method
    def testDrive(self):
        #add code so servo faces forward
        servo(self.MIDPOINT)
        #give the robot time to move
        time.sleep(.05)
        print("Here we go!")
        fwd()
        #start in an infinite loop
        #loop-- will continue until something gets in the way
        while True:
            #break the loop if the sensor reading is closer than our stop distance
            if us_dist(15) < self.STOP_DIST:
                self.stop()
                print("Ahhhhhh! All stop")
                if us_dist(15) < self.STOP_DIST:
                    break
            else:
                fwd()
                continue
                #you decide... how many seconds do you wait in between a check?
            time.sleep(.05)
            print("Seems clear, keep rolling")
            #stop if the sensor loop broke
        self.stop()


    #adding backup method
    #robot will back up a small amount if it gets too close to an object in its path
    def backUp(self):
        #if stop distance is less than 15, then it will back up
        if us_dist(15) < 15:
            print("Too close. Backing up for half a second")
            bwd()
            time.sleep(.5)
            self.stop()


    #calibrate robot
    #only use this code to calibrate robot, not within nav method
    #this method checks that my robot is looking straight ahead and that it is driving straight
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