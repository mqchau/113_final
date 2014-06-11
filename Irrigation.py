import GetIrvinePrecipitation
import WaterScheduler
import numpy as np

#Test
import ftplib, csv, threading, pprint, time, datetime, re

PF = 1.0
SF = 7250
IE = 0.75

#EV0 - EvapoTranspiration Value
#PF - Plant Factor
#SF - Square Feet
#0.62 - Constant Value for Conversion
#IE - Irrigation Efficiency

def getET0():
		dataList = GetIrvinePrecipitation.getIrvineWaterData()
		local_eto_array = list()
		for searchETo in dataList:
			#print str(searchETo['Reference ETo'])
			local_eto_array.append(searchETo['Reference ETo'])
			
		
		return sum(local_eto_array) / float(len(local_eto_array))
                #if (TIME IN DATABASE == CURRENT TIME)
                # if (dataList[searchETo]['Time'] == getCurrentVirtualTimeString()):
                        # ETo = dataList[searchETo]['ETo']
                        # print(ETo)
                        # return ETo

def getGalofWater():
	GalOfWat = (getET0()*PF*SF*0.62)/IE
	#print(GalOfWat)
	return GalOfWat

def getSchedule():
	min = round(getGalofWater()/46.0,1)
	if (min > 5):
		min = round(min/2.0, 1)
		duration = min
		schedule = [9,21]
	else:
		duration = min
		schedule = [20]
		
	return duration, schedule	
		
def main():
	#print "mean eto = " + str(getET0())
	#print(getGalofWater())
	dur, schedu = getSchedule()
	print str(dur) + "   " + str(schedu)

if __name__ == "__main__":
	main()
