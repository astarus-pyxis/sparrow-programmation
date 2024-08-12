"""

Sparrow - Programmation
Test du buzzer
Florian Topeza

"""

from buzzer import *
BUZZER_ENABLE = True

SetBuzzer(BUZZER_ENABLE, freq=2000, tps=1)
time.sleep(1)

SetBuzzer(False)
