from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0 #float: Threshold for the control of the orientation
d_th = 0.4 #float: Threshold for the control of the linear distance

fin_silver = [] #record the number of found silver token 
fin_gold = [] #record the number of found gold tokens

R = Robot() #instance of the class Robot

def forward(speed, seconds): 
    """
    This function is for moving forward
    Args:   speed (int): the speed of the wheels
	        seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    This function is for turning
    Args:   speed (int): the speed of the wheels
	        seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed/2
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(color): 
    """
    This function is for finding the closest token considering its color

    Arg:    color: true=silver false=gold

    Returns:dist (float): distance of the closest token (-1 if no token is detected)
           rot_y (float): angle between the robot and the token (-1 if no token is detected)
           num = offset
    """
    dist=100
    for token in R.see():
        if color == True and token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER: #silver and closer than previous token
            if token.info.offset in found_silver: #ignore tokens which are already been delivered
                continue
            else:
                dist=token.dist
                rot_y=token.rot_y
                num=token.info.offset #to distinguish token if it's delivered or not
        elif color == False and token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            if token.info.offset in found_gold: #ignore tokens which are already delivered
                continue
            else:
                dist=token.dist
                rot_y=token.rot_y
                num=token.info.offset
    if dist==100:
        return -1, -1, -1
    else:
        return dist, rot_y, num

def rem(color, num):

    """
    Args:   color:  silver=true, gold=false
            num:    offset of the token
    """
    if  color == False: #counts golds
        found_gold.append(num)
        print("REACHED GOLD: "+str(found_gold))
    elif   
        color == True: #counts silvers
        found_silver.append(num)
        print("REACHED SILVER: "+str(found_silver))

def main():
    print("MISSION STARTED!") 
    silver = True #look for silver at first
    while 1:
        dist, rot_y, num = find_token(silver) #info about closest token(silver/gold)
        if dist==-1: 
            print("NO TOKEN FOUND (YET)")
            turn(10,1)
        elif dist <d_th + 0.2: #if the robot is about to reach token, we grab/release it
            print("Found You!")
            if silver == True:
                forward(20, 1) #go forward a bit
                print("Got you!")
                R.grab() #grab silver token
                rem(silver, num) #recording its number
                turn(-20, 2)
                print("Time to deliver!")
            elif silver == False:
                print("Here you are!")
                R.release()
                rem(silver, num)
                if len(found_gold) == 6:
                    forward(-20, 2)
                    turn(+20, 1.5)
                    print("GJ!MISSION COMPLETED!")
                    exit()
                turn(+20, 2)
            silver = not silver #switch silver/gold
        elif -a_th<= rot_y <= a_th: 
            print("Good direction")
            forward(40, 0.5)
        elif rot_y > a_th:
            print("right")
            turn(+4, 0.25)
        elif rot_y < -a_th: 
            print("left")
            turn(-4, 0.25)
		
main()
