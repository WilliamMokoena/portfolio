from time import sleep
from MotorControl import activePositionings, cutterPositioning, defaultPos
from Kill import killSwitch as kill

# starts to check if the positionings are all at 0 if not Sets them to default

dtPos = defaultPos()
dtPos.setToDefault()
# *** Potential issues are since we are using the 1 switch to see is the Cutters Y and X positions are at default:
# ***  The code will activate both sets of motors since the Pi is receiving a signal from a single pin each

try:
    def userInter():
        cutter = input(
            'Select Your \n1. Laser Cutter \n2. Water Jet Cutter \n >> ')
        print(
            '\n\tPlease make sure that the material is Centered before begining cutting\n\n')

        def materialDim():
            print('\tSpecify the material dimensions in Milimeters\n')
            materialLen = input('Set Length : ')
            materialWid = input('\nSet Width : ')
            materialThickness = input('\nSet Thickness : ')
            Continue = input('\n\tType 0 to restart OR 1 to save \n >> ')

            if Continue == 0:
                materialDim()
            else:
                pass

            matDim = [materialLen, materialWid, materialThickness]

            return matDim

        def cuttingParameters():
            print('\tSpecify the cutting parameters \n')
            edges = int(input('Number of Edges : '))
            print('\n\tNote that Cutting Range has a margin of 110mm from the edges of the material\n\t of the material USE the allocated GRID MAP for your inputs\n')

            crdDict = {}
            print('\tSpecify Start and Stop Coordinates for cuttting\n\t<< Positives for forward Cuts >>\n\t<< Negatives for backward Cuts >>\n\n')

            for crd in range(1, edges + 1):
                xnum = int(input('Set xPoint : '))
                ynum = int(input('Set yPoint : '))
                crdDict['x{0}'.format(crd)] = xnum
                crdDict['y{0}'.format(crd)] = ynum

                Continue = input('\n\tType 0 to restart OR 1 to save \n >> ')
                if Continue == 00:
                    cuttingParameters()
                else:
                    pass

                crd += 1
                edscord = [crdDict, edges]
            return edscord

        def startCutting(matDim, crdDict, edges):
            startPos = cutterPositioning()
            startPos.yPos(crdDict['y1'], cutter)
            startPos.xPos(crdDict['x1'], cutter)
            startPos.zPos(matDim[2])

            act = int(input('\n\tEnter 1 to start or 0 to Abort\n >> '))
            cutting = activePositionings()

            if act == 1:
                run = 1
                cordListX = []
                cordListZ = []
                s = 0
                en = 0

                for cd in Dict:
                    if run == 1:
                        cordListX.append(Dict[cd])
                        run += 1

                    elif run == 2:
                        cordListZ.append(Dict[cd])
                        run = 1

                if cutter == 1:
                    print('\n\tCaution LASER Active Hit \n\n\t<< Ctrl+C to ABORT >>\n')

                elif cutter == 2:
                    print(
                        '\n\tCaution Water Jet Active Active Hit \n\n\t<< Ctrl+C to ABORT >>\n')

                while 1:
                    startPoint = [cordListX[s], cordListZ[s]]
                    endPoint = [cordListX[en], cordListZ[en]]
                    cutting.linearCutting(startPoint, endPoint, cutter)
                    s += 1
                    en += 1

                    if s == edges - 1 and en == edges - 1:
                        break

            elif act == 0:
                print('ABORTED')

        matDim = materialDim()
        edcrd = cuttingParameters()
        crdDict = edcrd[0]
        edges = edcrd[1]
        startCutting(matDim, crdDict)

        dtPos.setToDefault()

    userInter()

except KeyboardInterrupt:
    # KILL
    kill
