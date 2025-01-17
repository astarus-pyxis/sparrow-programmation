"""

Sparrow - Embedded systems programming
Test of the actuator
Florian Topeza

"""

from machine import Pin, PWM
import time

from servo_class import *

servo = SERVO(8)

servo.move_servo(servo.MAX) # change the position to MIN, MID or MAX to move the actuator
time.sleep(0.27)
servo.deinit()
