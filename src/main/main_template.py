"""
Sparrow - Embedded systems programming
Template for the main code of the rocket
Florian Topeza

"""

# This template gives you the outline of the code for your rocket.
# Feel free to use it to write your code.

# import the necessary libraries
from machine import Pin, I2C
import math
import time
import sys

# upload the files lps22hb.py and lsm6dsx.py if you use the new IMU and barometer (black board)
# otherwise upload the files imu.py and lps22hbtr.py (blue board)

# comment the two following lines if you use the new IMU and barometer (black board)
from MPU9250 import MPU9250
from lps22hbtr import LPS22HB

# uncomment the two following lines if you use the new IMU and barometer (black board)
#from lsm6dsx import LSM6DSx
#from lps22hb import LPS22HB

from servo_class import *
from buzzer import *

# variable for the buzzer
BUZZER_ENABLE = True

# buzzer for the start of the initialization
# TO DO
# Le buzzer shall buzz 1s à the frequency of 800Hz.


"""loop"""

if __name__ == '__main__':
    
    # creating objects for the IMU and barometer
    # comment the following lines if you use the new sensors
    imu = MPU9250()
    lps22hb = LPS22HB()

    # uncomment the following lines if you use the new IMU
    # /!\ contrary to the old sensors, the constructors of the new sensors take the I2C bus as
    # argument
    #i2c_bus = I2C(1,scl=Pin(7),sda=Pin(6),freq=400_000)
    #imu = LSM6DSx(i2c_bus)
    #lps22hb=LPS22HB(i2c_bus)
    
    # creating object for the actuator
    # Check on your board which pin is connected to the servo
    servo = SERVO(18) # for example, if the servo is connected to pin 18
    
    # variables for the main loop
    launched = 0
    parachute = 0
    alt = 0
    max_alt = 0
    count_descent = 0
    count_landed = 0
    last_alt = 0
    final_alt = 0
    landed = 0
    
    """Pressure and temperature"""
    PS = 0
    PRESS_DATA = 0.0
    TEMP_DATA = 0.0
    
    # lock the parachute compartment
    # TO DO

    # open data file in append mode, to write data without erasing data already in the file
    # TO DO
    
    # buzzer for the end of the initialization
    # TO DO
    # buzz 0.2s at the frequency of 600Hz
    
    # buzzer until launch
    # TO DO
    # buzz at 1000Hz every second
    
    # main loop
    while landed == 0:
        
        # comment the two following lines if you use the new IMU and barometer (black board)
        PRESS_DATA, TEMP_DATA = lps22hb.getData()
        ax, ay, az, pitch, roll, yaw = imu.getData()

        # uncomment the tree following lines if you use the new IMU and barometer (black board)
        #PRESS_DATA = lps22hb.pressure()
        #TEMP_DATA = lps22hb.temperature()
        #ax, ay, az, pitch, roll, yaw = imu.data()
            
        if PS == 0 :
            PS = PRESS_DATA
        
        last_alt = alt
        alt = 44330 * (1 - (PRESS_DATA / PS) ** 0.1903) # altitude calculation
        
        max_alt = max(alt, max_alt)
            
        
        """Display"""
        
        print("\r\n /-------------------------------------------------------------/ \r\n")
        print('\r\nPressure = %6.2f hPa , Static Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n'%(PRESS_DATA,PS,TEMP_DATA))
        print('\r\nAltitude = %6.1f m \r\n'%(alt))
        print('\r\nAltitude Max = %6.1f m \r\n'%(max_alt))
        print('\r\nRoll = %d , Pitch = %d , Yaw = %d\r\n'%(roll,pitch,yaw))
        print('\r\nAcceleration:  X = %.1f , Y = %.1f , Z = %.1f\r\n'%(ax, ay, az))
        print('\r\nLancé = %.1f , Parachute = %.1f\r\n'%(launched, parachute))
        
        """Engine"""
        # if the rocket detects a strong acceleration (more than 40m.s^(-2) in any direction), it considers it is being launched and the timer starts
        # TO DO
        # if (launched == ...) and (abs(ax) > 40 or ...):
        #    launched = ...
        #    start_time = ...
            
            # flight buzzer
            # TO DO
            # buzz every second at 1500Hz
            
        if launched == 1:
            
            # TO DO
            # Time of flight calculation
            # execution_time = temps_courant - start_time
            
            # the parachute deployment happens 7s after launch max
            # TO DO
            #if execution_time > ... and parachute == ...:
            #   parachute = ...
            # open parachute compartment
            # TO DO
               
               # buzzer for the parachute deployment
               # TO DO
               # 2000Hz for 0.5s
               
            # if apogee detected between 5s and 7s, deploy parachute 
            # TO DO
            # if execution_time > ... and parachute == ...:
            
            # TO DO
            # You shall detect a decrease in the altitude 5 times consecutively to consider that the rocket is going down and that the parachute shall be deployed.
            # If the altitude increases before decreasing 5 times consecutively, you have to reset the counter.
                    
                    #buzzer for the parachute deployment
                    # TO DO
                    # 2000Hz for 0.5s

            # Once the parachute has been deployed, landing is detected with 10 consecutive altitudes close of less than a meter to each other    
            if parachute == 1:
                if abs(final_alt - alt) < 1:
                    count_landed += 1
                    
                else :
                    final_alt = alt
                    count_landed = 0
                
                # landing has been detected, we close the file and escape the loop
                if count_landed > 10 :
                    landed = 1
                    file.close()
                    break

            # write the data in the file
            # do not forget to flush the file
            # TO DO   
            #file.write(str(execution_time) + "," + str(PRESS_DATA) + "," + ... + "\n")
    
    # buzzer off
    SetBuzzer(False)
