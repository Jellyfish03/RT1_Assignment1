
Repository aimed to contain the RT1 course work

Assignment1 RT1
================================

Introduction
------------

The task we have to accomplish is **to make the robot couple each silver token with each gold token**.

Installing 
----------

At first clone this repository in ur workspace.

The simulator requires a Python 2.7 and some libraries:
- [pygame](http://pygame.org/) 
- [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331)
- [PyYAML](https://pypi.python.org/pypi/PyYAML/).

to install them if you haven't already, follow the next command:

```bash
$ sudo pip2 install *name of the library*
```

if you meet some errors when you try installing some of the libraries, check if python2-dev is installed properly:

```bash
$ sudo apt-get install python2-dev
```

Running
-------

To run the assignment:

```bash
$ python2 run.py assignment1.py
```

Description of the Environment:
------------

In the environment you will find the following:

1. the robot
   
   ![alt text](https://github.com/kazu610/1st_assignment_RT1/blob/main/sr/robot.png)
2. the silver tokens
   
   ![alt text](https://github.com/kazu610/1st_assignment_RT1/blob/main/sr/token_silver.png)
3. the gold tokens
   
   ![alt text](https://github.com/kazu610/1st_assignment_RT1/blob/main/sr/token.png)

Robot API description
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

I personally implemented 2 functions to move the robot.

| NAME | FEATURE |
|:---------------:|:----------------:|
| `forward(speed, seconds)` | to move forward at `speed` for `seconds` |
| `turn(speed, seconds)` | to turn for `seconds` at angular velocity based on `speed` |

### Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).


Code Description
----------------

### Finding tokens knowing the color: the 'find_token' function ###


```python
def find_token(color): 
    """
    This function is for fiding the closest token considering its color

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
```

### Remembering reached tokens:   ###

In order to know which tokens the robot already reached, it needs to remember offsets of reached tokens.
`rem(color, num)` function receives the number given by the `find_token` function with argument `num`. If argument `color` is `false`, the number is stored in array `found_gold`. And if it's `true`, the number is stored in array `found_silver`. 

```python
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
    
```

### Main ###

The main function actually execute the task exploiting the functions that has just being described. The variable `silver` determines which color token to go. Based on tolerances `d_th` and `a_th`, the robot moves toward the target token. If the robot reached all tokens in the environment, the process is terminated with a message **GJ!MISSION COMPLETED!**.

```python
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
        
```

Flowchart
---------

![alt text](https://github.com/Jellyfish03/RT1_Assignment1/blob/main/Assignment1_RT1/Pics/Function.png)

### Move to Token process ###

![alt text](https://github.com/Jellyfish03/RT1_Assignment1/blob/main/Assignment1_RT1/Pics/Move%20to%20it.png)

