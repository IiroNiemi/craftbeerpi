import os
from subprocess import Popen, PIPE, call
from random import randint, uniform
from brewapp import app
from decimal import Decimal, ROUND_HALF_UP
from subprocess import call

class USBThermometer(object):

    def init(self):
        call("/opt/owfs/bin/owfs --allow_other -u -m /mnt/1wire")
        pass

    def getSensors(self):
        try:
            arr = []
            for dirname in os.listdir('/mnt/1wire'):
                if(dirname != "w1_bus_master1"):
                    arr.append(dirname)
            return arr
        except:
            return ["DummySensor1","DummySensor2"]

    def readTemp(self, tempSensorId):
        try:
            ## Test Mode
            if(tempSensorId == None or tempSensorId == ""):
                return -1
            if (app.testMode == True):
                pipe = Popen(["cat","w1_slave"], stdout=PIPE)
                result = pipe.communicate()[0]
            else:
                rtemp = open("/mnt/1wire/" + tempSensorId + "/temperature")
                result = rtemp.read()
                rtemp.close()
            if (result != None and result != ""):
                temp_C = float(result)
            else:
                temp_C = -99 #bad temp reading
        except Exception as e:
            temp_C = round(randint(0,50),2)

        return float(format(temp_C, '.2f'))