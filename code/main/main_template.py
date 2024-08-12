"""
Sparrow - Programmation
Template du code principal de la fusée
Florian Topeza

"""

# Ce template vous donne l'architecture du code principal à fournir pour contrôler votre fusée.
# Vous pouvez l'utiliser et le compléter pour écrire votre code.

# Importations
import machine
from machine import Pin, I2C
import math
import time
import sys

from MPU9250 import MPU9250 # Librairie pour l'IMU
from lps22hbtr import LPS22HB # Librairie pour l'IMU
from servo_class import * # Importation des fonctions pour contrôler le servomoteur
from buzzer import * # Importation des fonctions pour contrôler le buzzer

#définition de la variable du buzzer
BUZZER_ENABLE = True

#buzzer de début d'initialisation
# A COMPLETER
# Le buzzer doit sonner 1s à la fréquence de 800Hz.


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
    # A COMPLETER
    # Faire tourner le servo pour verrouiller la trappe

    # Ouvrir le fichier pour écrire les données de vol
    # A COMPLETER
    # Assurez-vous d'ouvrir le fichier en mode append et pas write, pour éviter de perdre des données déjà enregistrées.
    
    #buzzer de fin d'initialisation
   # A COMPLETER
   # Buzzer 0.2s à la fréquence de 600Hz
    
    #buzzer jusqu'au décollage
    # A COMPLETER
    # Buzzer à 1000Hz toutes les secondes
    
    #boucle principale
    while landed == 0:
        PRESS_DATA, TEMP_DATA = lps22hb.getData()
        ax, ay, az, pitch, roll, yaw = mpu9250.getData()
            
        if PS == 0 :
            PS = PRESS_DATA
        
        last_alt = alt
        alt = 44330 * (1 - (PRESS_DATA / PS) ** 0.1903) # Calcul de l'altitude
        
        max_alt = max(alt, max_alt)
            
        
        # Commande d'affichage des données, utile lorsque vous testerez le code avec la carte branchée à Thonny.
        """affichage"""
        
        print("\r\n /-------------------------------------------------------------/ \r\n")
        print('\r\nPressure = %6.2f hPa , Static Pressure = %6.2f hPa , Temperature = %6.2f °C\r\n'%(PRESS_DATA,PS,TEMP_DATA))
        print('\r\nAltitude = %6.1f m \r\n'%(alt))
        print('\r\nAltitude Max = %6.1f m \r\n'%(max_alt))
        print('\r\nRoll = %d , Pitch = %d , Yaw = %d\r\n'%(roll,pitch,yaw))
        print('\r\nAcceleration:  X = %.1f , Y = %.1f , Z = %.1f\r\n'%(ax, ay, az))
        print('\r\nLancé = %.1f , Parachute = %.1f\r\n'%(launched, parachute))
        
        """Moteur"""
        
        # Si l'état est avant décollage et qu'une accélération de plus de 40m.s^(-2) est détectée dans une direction,
        # l'état de la carte passe en vol et le timer se lance
        # A COMPLETER
        # if (launched == ...) and (abs(ax) > 40 or ...):
        #    launched = ...
        #    start_time = ...
            
            #buzzer de vol
            # A COMPLETER
            # Buzzer toutes les secondes à 1500Hz
            
        if launched :
            
            # A COMPLETER
            # Calcul du temps de vol
            # exectution_time = temps_courant - start_time
            
            # Ouverture du parachute au bout de 7s au plus tar
            # A COMPLETER
            #if execution_time > ... and parachute == ...: #si on dépasse la plage de temps accordée pour le déploiement du parachute, on le déploit quand même
            #   parachute = ...
            # Ouverture de la trappe
            # A COMPLETER
               
               #buzzer de déploiement du parachute
               # A COMPLETER
               # Buzzer à 2000Hz pendant 0.5s
               
            # Si entre 5s et 7s de vol, l'apogée est détecté, ouvrir le parachute à ce moment.
            # A COMPLETER
            # if execution_time > ... and parachute == ...: #si on détecte l'apogée dans la plage de temps, on déploit le parachute
            
            # A COMPLETER
            # Vous devez détecter une diminution de l'altitude 5 fois de suite pour considérer que la fusée redescend et qu'il faut
            # ouvrir le parachute.
            # Si l'altitude remonte avant 5 diminutions consécutives, il faut recommencer à 0.
                    
                    #buzzer de déploiement du parachute
                    # A COMPLETER
                    # Buzzer 2000Hz pendant 0.5s

            # Une fois le parachute déploy", on détecte l'atterrissage par 10 altitudes consecutives proches de moins de 1m
            # les unes des autres.      
            if parachute == 1:
                if abs(final_alt - alt) < 1:
                    count_landed += 1
                    
                else :
                    final_alt = alt
                    count_landed = 0
                
                if count_landed > 10 : #l'atterrissage est détecté, on ferme le fichier data et on sort de la boucle while
                    landed = 1
                    file.close()
                    break

            # Ecriture des données de vol dans le fichier
            # A COMPLETER   
            #file.write(str(execution_time) + "," + str(PRESS_DATA) + "," + ... + "\n")
    
    # Extinction du buzzer
    SetBuzzer(False)
