"""

Sparrow - Embedded systems programming
Test of the accelerometer
Florian Topeza

"""


from machine import Pin
import time

accPin = Pin(28, Pin.IN)

accContact = False

def IrqAcc(p):
    global accContact
    accContact = True
    print("contact")

accPin.irq(trigger=Pin.IRQ_RISING, handler = IrqAcc)
time.sleep(20)