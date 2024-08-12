"""
Sparrow - Programmation
Code principal de la fusée
Florian Topeza

"""

import machine
from machine import Pin, I2C
import math
import time
import sys

"""import files"""
from MPU9250 import MPU9250
from lps22hbtr import LPS22HB
from servo_class import *
from buzzer import *

#définition de la variable du buzzer
BUZZER_ENABLE = True

#buzzer de début d'initialisation
SetBuzzer(BUZZER_ENABLE, freq=800, tps=1)
time.sleep(1)
SetBuzzer(False)


"""boucle"""

if __name__ == '__main__':
    
    #définitions des variables de classes pour l'IMU
    mpu9250 = MPU9250()
    lps22hb=LPS22HB()
    
    #définition de la variable de classe du servo
    servo = SERVO(10)
    
    #définition des variables utiles pour la boucle principale
    launched = 0
    parachute = 0
    alt = 0
    max_alt = 0
    count_descent = 0
    count_landed = 0
    last_alt = 0
    final_alt = 0
    landed = 0
    
    """pression et température"""
    PS = 0
    PRESS_DATA = 0.0
    TEMP_DATA = 0.0
    u8Buf=[0,0,0]
    
    #on verouille la trappe
    servo.move_servo(servo.MID)
    time.sleep(0.27)
    servo.deinit()

    # Ouvrir le fichier en mode écriture
    file = open("data.csv", "a")
    file.write("execution_time,Pressure,Altitude,Acceleration X,Acceleration Y,Acceleration Z,Pitch,Roll,Yaw,Parachute\n")
    
    
    #buzzer de fin d'initialisation
    SetBuzzer(BUZZER_ENABLE, freq=800, tps=0.2)
    time.sleep(0.6)
    
    #buzzer jusqu'au décollage
    SetBuzzer(BUZZER_ENABLE, freq=1000, tps=0.2)
    
    
    #boucle principale
    while landed == 0:
        PRESS_DATA, TEMP_DATA = lps22hb.getData()
        ax, ay, az, pitch, roll, yaw = mpu9250.getData()
            
        if PS == 0 :
            PS = PRESS_DATA
        
        last_alt = alt
        alt = 44330 * (1 - (PRESS_DATA / PS) ** 0.1903)
        
        max_alt = max(alt, max_alt)
            
        
        
        """affichage"""
        
        print("\r\n /-------------------------------------------------------------/ \r\n")
        print('\r\nPressure = %6.2f hPa , Static Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n'%(PRESS_DATA,PS,TEMP_DATA))
        print('\r\nAltitude = %6.1f m \r\n'%(alt))
        print('\r\nAltitude Max = %6.1f m \r\n'%(max_alt))
        print('\r\nRoll = %d , Pitch = %d , Yaw = %d\r\n'%(roll,pitch,yaw))
        print('\r\nAcceleration:  X = %.1f , Y = %.1f , Z = %.1f\r\n'%(ax, ay, az))
        print('\r\nLancé = %.1f , Parachute = %.1f\r\n'%(launched, parachute))
        
        """Moteur"""
        
        # si l'état est avant décollage et qu'on détecte une forte accélération, l'état de la carte passe en vol et le timer se lance
        if (launched == 0) and (abs(ax) > 40 or abs(ay) > 40 or abs(az) > 40):
            launched = 1
            start_time = time.ticks_ms()
            
            #buzzer de vol
            SetBuzzer(BUZZER_ENABLE, freq=1500, tps=1)
            
        if launched :
            end_time = time.ticks_ms()
            execution_time = time.ticks_diff(end_time, start_time)/1000 #calcul du temps de vol
            
            if execution_time > 7 and parachute == 0: #si on dépasse la plage de temps accordée pour le déploiement du parachute, on le déploit quand même
               parachute = 1
               servo.move_servo(servo.MIN)
               time.sleep(0.27)
               servo.deinit()
               
               #buzzer de déploiement du parachute
               SetBuzzer(BUZZER_ENABLE, freq=2000, tps=0.5)
               
            if execution_time > 5 and parachute == 0: #si on détecte l'apogée dans la plage de temps, on déploit le parachute
                if alt < last_alt :
                    count_descent += 1
                else :
                    count_descent = 0
                    
                if count_descent > 5 : #détection de l'apogée
                    parachute = 1
                    servo.move_servo(servo.MIN)
                    time.sleep(0.27)
                    servo.deinit()
                    
                    #buzzer de déploiement du parachute
                    SetBuzzer(BUZZER_ENABLE, freq=2000, tps=0.5)
                    
            if parachute == 1: #si le parachute est déployé, on essaye de détecter l'atterrissage
                if abs(final_alt - alt) < 1:
                    count_landed += 1
                    
                else :
                    final_alt = alt
                    count_landed = 0
                
                if count_landed > 10 : #l'atterrissage est détecté, on ferme le fichier data et on sort de la boucle while
                    landed = 1
                    file.close()
                    break
                
            file.write(str(execution_time) + "," + str(PRESS_DATA) + "," + str(alt) + "," + str(ax) + "," + str(ay) + "," + str(az) + "," + str(pitch) + "," + str(roll) + "," + str(yaw) + "," + str(parachute) + "\n")
    SetBuzzer(False)
