"""
Sparrow - Embedded systems programming
Main code of the rocket
Florian Topeza

"""

import machine
from machine import Pin, I2C
import math
import time
import sys

"""import files"""

# use the files lps22hb.py and lsm6dsx.py if you use the new IMU and barometer
# otherwise use the files MPU9250.py and lps22hbtr.py

# comment the two following lines if you use the new IMU and barometer
from MPU9250 import MPU9250
from lps22hbtr import LPS22HB

# uncomment the two following lines if you use the new IMU and barometer
#from lsm6dsx import LSM6DSx
#from lps22hb import LPS22HB

from servo_class import *
from buzzer import *

# variable for the buzzer
BUZZER_ENABLE = True

# buzzer for the start of the initialization
SetBuzzer(BUZZER_ENABLE, freq=800, tps=1)
time.sleep(1)
SetBuzzer(False)


"""loop"""

if __name__ == '__main__':
    
    # creating objects for the IMU and barometer
    # comment the following line if you use the new IMU
    mpu9250 = MPU9250()
    # uncomment the following line if you use the new IMU
    #mpu9250 = L6M6DSx()
    lps22hb=LPS22HB()
    
    # creating object for the actuator
    servo = SERVO(10)
    
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
    u8Buf=[0,0,0]
    
    # lock the parachute compartment
    servo.move_servo(servo.MID)
    time.sleep(0.27)
    servo.deinit()

    # open data file in append mode, to write data without erasing data already in the file
    file = open("data.csv", "a")
    file.write("execution_time,Pressure,Altitude,Acceleration X,Acceleration Y,Acceleration Z,Pitch,Roll,Yaw,Parachute\n")
    
    
    # buzzer for the end of the initialization
    SetBuzzer(BUZZER_ENABLE, freq=800, tps=0.2)
    time.sleep(0.6)
    
    # buzzer until launch
    SetBuzzer(BUZZER_ENABLE, freq=1000, tps=0.2)
    
    
    #main loop
    while landed == 0:

        # comment the two following lines if you use the new IMU and barometer
        PRESS_DATA, TEMP_DATA = lps22hb.getData()
        ax, ay, az, pitch, roll, yaw = mpu9250.getData()

        # uncomment the tree following lines if you use the new IMU and barometer
        #PRESS_DATA = lps22hb.pressure()
        #TEMP_DATA = lps22hb.temperature()
        #ax, ay, az, pitch, roll, yaw = mpu9250.data()


        if PS == 0 :
            PS = PRESS_DATA
        
        last_alt = alt
        alt = 44330 * (1 - (PRESS_DATA / PS) ** 0.1903)
        
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
        
        # if the rocket dectects a strong acceleration, it considers it is being launched and the timer starts
        if (launched == 0) and (abs(ax) > 40 or abs(ay) > 40 or abs(az) > 40):
            launched = 1
            start_time = time.ticks_ms()
            
            # flight buzzer
            SetBuzzer(BUZZER_ENABLE, freq=1500, tps=1)
            
        if launched :
            end_time = time.ticks_ms()
            execution_time = time.ticks_diff(end_time, start_time)/1000 # time of flight calculation
            
            # the parachute deployment happens 7s after launch max
            if execution_time > 7 and parachute == 0:
               parachute = 1
               servo.move_servo(servo.MIN)
               time.sleep(0.27)
               servo.deinit()
               
               # buzzer for the parachute deployment
               SetBuzzer(BUZZER_ENABLE, freq=2000, tps=0.5)

            # if apogee detected, deploy parachute  
            if execution_time > 5 and parachute == 0:
                if alt < last_alt :
                    count_descent += 1
                else :
                    count_descent = 0

                # apogee detection  
                if count_descent > 5 :
                    parachute = 1
                    servo.move_servo(servo.MIN)
                    time.sleep(0.27)
                    servo.deinit()
                    
                    #buzzer for the parachute deployment
                    SetBuzzer(BUZZER_ENABLE, freq=2000, tps=0.5)

            # if parachute deployed, try to detect landing        
            if parachute == 1:
                if abs(final_alt - alt) < 1:
                    count_landed += 1
                    
                else :
                    final_alt = alt
                    count_landed = 0
                
                # detected landing, close file and escape while loop
                if count_landed > 10 :
                    landed = 1
                    file.close()
                    break
                
            file.write(str(execution_time) + "," + str(PRESS_DATA) + "," + str(alt) + "," + str(ax) + "," + str(ay) + "," + str(az) + "," + str(pitch) + "," + str(roll) + "," + str(yaw) + "," + str(parachute) + "\n")
    
    # buzzer off
    SetBuzzer(False)
