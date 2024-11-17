from machine import Pin,PWM

class SERVO():

    MID = 1500000
    MIN = 600000
    MAX = 2200000
    
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
    
    def move_servo(self, ns):
        self.pwm.duty_ns(ns)

    def deinit(self):
        self.pwm.deinit()
