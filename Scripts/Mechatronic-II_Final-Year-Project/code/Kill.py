from time import sleep
import RPi.GPIO as gpio

from MotorControl import activePositionings, cutterPositioning, defaultPos
from CutterToggle import toggle


class killSwitch:

    def whichActive(self):
