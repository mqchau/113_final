import sched, time, datetime, thread
import RPi.GPIO as GPIO
import GetIrvinePrecipitation
import Irrigation
import IrrigationPeripheral
import UpdateHTML
import subprocess
import PythonHTTP

s = sched.scheduler(time.time, time.sleep)
start_time = time.time()#datetime.datetime.now()
virtual_time = time.time()
days_passed = 1
scheduler_running = False
one_hour_factor = 10			#we convert 1 hour in to 10 seconds delay only, if you put 3600 here it will be real delay
num_LCD_updates = 2
LCD_interval = 5		#10 seconds to cycle, this is in real time, not virtual

current_schedule = None
irrigate_duration = 0

def getIpAddress():
	arg='ip route list'
	p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
	data = p.communicate()
	split_data = data[0].split()
	ipaddr = split_data[split_data.index('src')+1]
	return ipaddr
	
def waterZone1():
	IrrigationPeripheral.turnOnLED()
	time.sleep(irrigate_duration * 60)		#let the LED on the correct amount of time
	IrrigationPeripheral.turnOffLED()
	IrrigationPeripheral.flash(0.4)
	#print "Watering zone 1 at " + getCurrentVirtualTimeString()

def UpdateHTMLPage():
	global irrigate_duration
	UpdateHTML.UpdateHTML(getCurrentVirtualTimeString(), str(IrrigationPeripheral.get_current_temp()), str(irrigate_duration), [20], GetIrvinePrecipitation.getIrvineWaterData())
	
def LcdUpdate1():
	global LCD_interval
	IrrigationPeripheral.lcd_write_top(getCurrentVirtualTimeString())
	IrrigationPeripheral.lcd_write_bottom("temp = " + str(IrrigationPeripheral.get_current_temp()) + " F")
	# print "Updating LCD with string 1"
	# print "virtual_time = " + getCurrentVirtualTimeString()
	# print "real_time = " + time.ctime(time.time())
	s.enter(LCD_interval, 1, LcdUpdate2, ())
	

def LcdUpdate2():
	global LCD_interval, irrigate_duration
	IrrigationPeripheral.lcd_write_top("duration=" + str(irrigate_duration) + "min")
	string_bottom = "at "
	for one in current_schedule:
		string_bottom = string_bottom + str(one) + ":00 "
	IrrigationPeripheral.lcd_write_bottom(string_bottom)
	# print "Updating LCD with string 2"	
	# print "virtual_time = " + getCurrentVirtualTimeString()
	# print "real_time = " + time.ctime(time.time())
	s.enter(LCD_interval, 1, LcdUpdate3, ())
	
def LcdUpdate3():
	IrrigationPeripheral.lcd_write_top("Auto Irrigation")
	IrrigationPeripheral.lcd_write_bottom(getIpAddress())	
	s.enter(LCD_interval, 1, LcdUpdate1, ())
	
	
def waterAllZone():
	waterZone1()
	
def calculateNewSchedule():
	global days_passed, s, irrigate_duration
	#print "calculateNewSchedule at " + getCurrentVirtualTimeString()
	irrigate_duration, new_schedule = Irrigation.getSchedule()			#only change this line to call actual method
	days_passed = days_passed + 1
	current_schedule = new_schedule
	setOneDaySchedule(0, new_schedule)
	
def getCurrentVirtualTimeString():
	global start_time, one_hour_factor
	return time.ctime((time.time() - start_time)/one_hour_factor * 3600 + start_time)
	
def applyHourFactor(time_float):
	global start_time, one_hour_factor
	return (time_float - start_time) * one_hour_factor / 3600 + start_time
		
def setOneDaySchedule(offset, schedule_list):
	global s, start_time, one_hour_factor, scheduler_running, virtual_time
	
	#get current hour	
	virtual_datetime = datetime.datetime.fromtimestamp(time.mktime(time.localtime(virtual_time)))	
	
	#set time to water zone
	for one in schedule_list:
		predicted_datetime = virtual_datetime.replace(hour = one, minute = 0, second = 0)
	
		predicted_time = time.mktime(predicted_datetime.timetuple())
		if  predicted_time < virtual_time:			
			predicted_time = predicted_time + 24 * 3600			#advance 24 hr if that time has passed
		s.enterabs(applyHourFactor(predicted_time), 1, waterAllZone, ())				
		
	#set time to get new data and get new schedule
	s.enterabs(start_time + days_passed * 24 * one_hour_factor, 1, calculateNewSchedule, ())

	virtual_time = virtual_time + 24 * 3600
	
	#run schedule
	if not scheduler_running:
		#set time to alternatively display LCD
		s.enter(0, 1, LcdUpdate1, ())
		
		#set time to update the HTML page
		s.enter(0, 1, UpdateHTMLPage,())
		
		
		
		scheduler_running = True
		s.run()					#Expect this: it'll be stuck here forever

if __name__ == "__main__":
	global irrigate_duration, current_schedule
	GPIO.setmode(GPIO.BCM)
	IrrigationPeripheral.initializePeripheral()	
	IrrigationPeripheral.lcd_init()
	IrrigationPeripheral.turnOffLED()	
	PythonHTTP.runServer()
		
	irrigate_duration , current_schedule = Irrigation.getSchedule()
	UpdateHTMLPage()
	
	setOneDaySchedule(0, current_schedule)
