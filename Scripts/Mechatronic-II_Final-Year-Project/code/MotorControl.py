import RPi.GPIO as gpio
from time import sleep

from CutterToggle import toggle as tg


def initZmotors():

    # Speicifying that the on-board physical pin numbering will be used
    gpio.setmode(gpio.BOARD)

    # Specifying the pins on the board that will be used (OUTPUT PINS) for the Z-axis motors
    gpio.setup(29, gpio.OUT)
    gpio.setup(31, gpio.OUT)
    gpio.setup(33, gpio.OUT)
    gpio.setup(35, gpio.OUT)


def initiateLaser():
    gpio.setmode(gpio.BOARD)

    # Specifying the pins on the board that will be used (OUTPUT PINS) for the laser's X-axis motor
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

    # Specifying the pins on the board that will be used (OUTPUT PINS) for the laser's Y-axis motor
    gpio.setup(12, gpio.OUT)
    gpio.setup(16, gpio.OUT)


def initiateWaterJet():
    gpio.setmode(gpio.BOARD)

    # Specifying the pins on the board that will be used (OUTPUT PINS) for the water-jet X-axis motor
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

    # Specifying the pins on the board that will be used (OUTPUT PINS) for the water-jet Y-axis motor
    gpio.setup(18, gpio.OUT)
    gpio.setup(22, gpio.OUT)


class motorPlane:

    def xAxis(self, direction, cutter):

        # Laser X-Axis movement

        def laserForwardX(self):
            initiateLaser()
            laserForwardX = gpio.PWM(7, 100)
            return laserForwardX

        def laserReverseX(self):
            initiateLaser()
            laserReverseX = gpio.PWM(11, 100)
            return laserReverseX

        # Water Jet X-Axis movement

        def waterJetForwardX(self):
            initiateWaterJet()
            waterJetForwardX = gpio.PWM(13, 100)
            return waterJetForwardX

        def waterJetreverseX(self):
            initiateWaterJet()
            waterJetreverseX = gpio.PWM(15, 100)
            return waterJetreverseX

        if direction == 'F' and cutter == 'LW':
            return [laserForwardX(self), waterJetForwardX(self)]
        elif direction == 'R' and cutter == 'LW':
            return [laserReverseX(self), waterJetReverseX(self)]

        if direction == 'F' and cutter == 'L':
            return laserForwardX(self)
        elif direction == 'R' and cutter == 'L':
            return laserReverseX(self)

    	if direction == 'F' and cutter == 'W':
            return waterJetForwardX(self)
        elif direction == 'R' and cutter == 'W':
            return waterJetReverseX(self)


    def yAxis(self, direction, cutter):

        def laserForwardY(self):
            initiateLaser()
            laserForwardY = gpio.PWM(12, 100)
            return laserForwardY

        def laserReverseY(self):
            initiateLaser()
            laserReverseY = gpio.PWM(16, 100)
            return laserReverseY

        def waterJetForwardY(self):
            initiateWaterJet()
            waterJetForwardY = gpio.PWM(18, 100)
            return waterJetForwardY

        def waterJetReverseY(self):
            initiateWaterJet()
            waterJetReverseY = gpio.PWM(22, 100)
            return waterJetReverseY

        if direction == 'F' and cutter == 'LW':
            return [laserForwardY(self), waterJetForwardY(self)]
        elif direction == 'R' and cutter == 'LW':
            return [laserReverseY(self), waterJetReverseY(self)]

        if direction == 'F' and cutter == 'L':
            return laserForwardY(self)
        elif direction == 'R' and cutter == 'L':
            return laserReverseY(self)

    	if direction == 'F' and cutter == 'W':
            return waterJetForwardY(self)
        elif direction == 'R' and cutter == 'W':
            return waterJetReverseY(self)

    def zAxis(self, direction):

        def forward(self):
            initZmotors()
            forward = [gpio.PWM(29, 100), gpio.PWM(35, 100)]
            return forward

        def reverse(self):
            initZmotors()
            reverse = [gpio.PWM(31, 100), gpio.PWM(33, 100)]
            return reverse

        if direction == 'F':
            forward(self)
        if direction == 'R':
            reverse(self)


activteMotor = motorPlane()


class defaultPos:

    def testXAPins(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)

        gpio.setup(19, gpio.IN, pull_up_down = gpio.PUD_UP) # laser X-axis motor
        gpio.setup(21, gpio.IN, pull_up_down = gpio.PUD_UP) # water jet X-axis

        if gpio.input(19) == 1 and gpio.input(21) == 1:
            return True
        else:
            return False

    def testYAPins(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)
        
        gpio.setup(23, gpio.IN, pull_up_down = gpio.PUD_UP) # laser Y-axis motor
        gpio.setup(26, gpio.IN, pull_up_down = gpio.PUD_UP) # water jet Y-axis motor

        if gpio.input(23) == 1 and gpio.input(26) == 1:
            return True
        else:
            return False

    def testZAPin(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)

        gpio.setup(24, gpio.IN, pull_up_down = gpio.PUD_UP) # Z-axis motor

        if gpio.input(24) == 1:
            return True
        else:
            return False

    def checkState(self):
        results = {'xaAtDefault': testXAPins(self),
                   'yaAtDefault': testYAPins(self),
                   'zaAtDefault': testZAPins(self)}

        for motor in results:
            if results['xaAtDefault'] == False:
                XA = False
            else:
                XA = True

            if results['yaAtDefault'] == False:
                YA = False
            else:
                YA = True

            if results['zaAtDefault'] == False:
                ZA = False
            else:
                ZA = True

            return XA, YA, ZA

    def setToDefault(self):

        def xSetToDefault(self):
            while XA == False:
                Set = activateMotor.xAxis(self, 'R', 'LW')
                Set[0].start(0), Set[1].start(0)
                Set[0].ChangeDutyCycle(70), Set[1].ChangeDutyCycle(70)
                sleep(.008 )
                Set[0].stop(), Set[1].stop()
                checkState(self)
                results = list(checkState(self))
                XA = results[0]
                if XA == True:
                    break

        def ySetToDefault(self):
            while YA == False:
                Set = activateMotor.yAxis(self, 'R', 'LW')
                Set.start(0)
                Set[0].start(0), Set[1].start(0)
                Set[0].ChangeDutyCycle(70), Set[1].ChangeDutyCycle(70)
                sleep(.008)
                Set[0].stop(), Set[1].stop()
                checkState(self)
                results = list(checkState(self))
                YA = results[1]
                if YA == True:
                    break


        def zSetToDefault(self):
            while ZA == False:
                Set = activateMotor.zAxis(self, 'R')
                Set.start(0)
                Set.ChangeDutyCycle(70)
                sleep(.008 )
                Set.stop()
                checkState(self)
                results = list(checkState(self))
                ZA = results[1]
                if ZA == True:
                    break

        results = list( checkState(self) )
        XA = results[0]
        YA = results[1]
        ZA = results[2]

        
        if YA == False:
            ySetToDefault(self)
        else:
            return True

        if XA == False:
            xSetToDefault(self)
        else:
            return True

        if ZA == False:
            zSetToDefault(self)
        else:
            return True


class cutterPositioning:

    # Setting the initial position for the cutter

    def xPos(self, materialLen, cutter):
        margin = (1547 - materialLen)/2
        dur = (margin / 54.93033225) * 0.066

        move = activteMotor.xAxis(self, 'F', cutter)
        move.start(0)
        move.ChangeDutyCycle(70)
        sleep(dur)
        move.stop()

        return margin

    def yPos(self, materialThickness):  
        margin = 310.42 - materialThickness
        dur = ((margin + 54.93033225*2) / 54.93033225) * 0.066

        move = activteMotor.yAxis(self, 'F', cutter)
        move.start(0)
        move.ChangeDutyCycle(70)
        sleep(dur)
        move.stop()

        return margin

    def zPos(self, materialWid, cutter): 
        margin = (1547 - materialWid)/2
        dur = ((margin + 54.93033225*2) / 54.93033225) * 0.066
        
        move = activteMotor.zAxis(self, 'F', cutter)
        move.start(0)
        move.ChangeDutyCycle(70)
        sleep(dur)
        move.stop()


class activePositionings:

    # Loops for how to move the cutter when cutting

    def linearCutting(self, startPoint, endPoint, toggleCutter):

        if startPoint[0] == endPoint[0]:

            if toggleCutter == 1:
                tg.LaserCutterToggle('ON')

            elif toggleCutter == 2:
                tg.WaterJetCutterToggle('ON')

            # X in Constant
            if startPoint[0] > 0:
                dur = startPoint[0] * 0.066

            elif startPoint[0] < 0:
                dur = startPoint[0] * -0.066

            if startPoint[1] > 0 and endPoint[1] > 0:
                move = activteMotor.zAxis(self, 'F', cutter)
                move.start(0)
                move.ChangeDutyCycle(80)
                sleep(dur)
                move.stop()

            elif startPoint[1] < 0 and endPoint[1] < 0:
                move = activteMotor.zAxis(self, 'R', cutter)
                move.start(0)
                move.ChangeDutyCycle(80)
                sleep(dur)
                move.stop()

        if startPoint[1] == endPoint[1]:

            if toggleCutter == 1:
                tg.LaserCutterToggle('ON')

            if toggleCutter == 2:
                tg.WaterJetCutterToggle('ON')

            # Z in Constant
            dur = startPoint * 0.066

            if startPoint[1] > 0 and endPoint[1] > 0:
                move = activteMotor.xAxis(self, 'F', cutter)
                move.start(0)
                move.ChangeDutyCycle(80)
                sleep(dur)
                move.stop()

            if startPoint[1] < 0 and endPoint[1] < 0:
                move = activteMotor.xAxis(self, 'R', cutter)
                move.start(0)
                move.ChangeDutyCycle(80)
                sleep(dur)
                move.stop()
        else:
            return 'FunNavError'



    def archCutting(self, startPoint, endPoint):

    def angledCutting(self, startPoint, endPoint):
