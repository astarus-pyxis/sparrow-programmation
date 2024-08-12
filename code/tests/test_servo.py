"""

Sparrow - Programmation
Test du servomoteur
Florian Topeza

"""

from machine import Pin, PWM
import time

from servo_class import *

servo = SERVO(10)

servo.move_servo(servo.MIN)
time.sleep(0.27)
servo.deinit()
