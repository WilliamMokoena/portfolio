import RPi.GPIO as gpio

class toggle:
    def LaserCutterToggle(self, OnOff):
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        gpio.setup(10, gpio.OUT)

        if OnOff == 'ON':
            gpio.output(10, gpio.HIGH)

        if OnOff == 'OFF':
            gpio.output(10, gpio.LOW)

    def WaterJetCutterToggle(self, OnOff):
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)
        gpio.setup(8, gpio.OUT)

        if OnOff == 'ON':
            gpio.output(8, gpio.HIGH)

        if OnOff == 'OFF':
            gpio.output(8, gpio.LOW)
