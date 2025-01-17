"""

Sparrow - Embedded systems programming
Test of the buzzer
Florian Topeza

"""

from buzzer import *
BUZZER_ENABLE = True

SetBuzzer(BUZZER_ENABLE, freq=2000, tps=1) # change frequency freq or period tps
time.sleep(3)

SetBuzzer(False)
