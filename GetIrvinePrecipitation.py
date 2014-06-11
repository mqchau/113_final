import ftplib, csv, threading, pprint, time, datetime, re

#this module's variable
IrvineWaterDataRaw = ''

# global ValidFlag, ValidFlagLock, IrvineWaterData

def processIrvineWaterData():
# We're using hourly in this module
#*******************************************
# DAILY Default 
# Order of Data:
# Column 
# letter/number   Sensor/Field
# ========================================
  # A   1.  	Station Id
  # B   2. 	Date
  # C   3. 	Julian Date
  # D   4.  	Reference ETo    
  # E   5.  	QC for Reference ETo              
  # F   6.  	Precipitation                     
  # G   7.  	QC for Precipitation              
  # H   8.  	Solar Radiation Average           
  # I   9.  	QC for Solar Radiation Average    
  # J   10. 	Average Vapor Pressure             
  # K   11. 	QC for Average Vapor Pressure     
  # L   12. 	Maximum Air Temperature           
  # M   13. 	QC for Maximum Air Temperature    
  # N   14. 	Minimum Air Temperature            
  # O   15. 	QC for Minimum Air Temperature    
  # P   16. 	Average Air Temperature
  # Q   17. 	QC for Average Air Temperature
  # R   18. 	Maximum Relative Humidity
  # S   19. 	QC for Maximum Relative Humidity
  # T   20. 	Minimum Relative Humidity 
  # U   21. 	QC for Minimum Relative Humidity
  # V   22. 	Average Relative Humidity  
  # W   23. 	QC for Average Relative Humidity
  # X   24. 	Dew Point
  # Y   25. 	QC for Dew Point
  # Z   26. 	Average Wind Speed 
  # AA  27. 	QC for Average Wind Speed
  # AB  28. 	Wind Run 
  # AC  29. 	QC for Wind Run
  # AD  30. 	Average Soil Temperature
  # AE  31. 	QC for Average Soil Temperature

# HOURLY Default
# Order of Data:
# Column 
# letter/number   Sensor/Field
# ========================================
  # A   1.  	Station Id
  # B   2.  	Date
  # C   3.  	Hour
  # D   4.  	Julian Date
  # E   5.  	Reference ETo
  # F   6.  	QC for Reference ETo
  # G   7.  	Precipitation
  # H   8.  	QC for Precipitation
  # I   9.  	Solar Radiation 
  # J   10. 	QC for Solar Radiation 
  # K   11. 	Vapor Pressure 
  # L   12. 	QC for Vapor Pressure
  # M   13. 	Air Temperature 
  # N   14. 	QC for Air Temperature
  # O   15. 	Relative Humidity 
  # P   16. 	QC for Relative Humidity
  # Q   17. 	Dew Point 
  # R   18. 	QC for Dew Point
  # S   19. 	Wind Speed 
  # T   20. 	QC for Wind Speed
  # U   21. 	Wind Direction 
  # V   22. 	QC for Wind Direction
  # W   23. 	Soil Temperature
  # X   24. 	QC for Soil Temperature
	global IrvineWaterDataRaw
	IrvineWaterData = list()
	# splitted_data = csv.reader(IrvineWaterDataRaw, delimiter=',')
	splitted_data = IrvineWaterDataRaw.split('\n')
	for row in splitted_data:
		if re.search("--", row):
			continue
		row = row.strip()
		col = row.split(',')
		
		if len(col) >= 24:
			new_hourly_data = dict()
			local_date = datetime.datetime.strptime(col[1], "%m/%d/%Y")
			# print col[1] + "  " + col[ 2]
			if col[ 2] == "2400":				
				local_date = local_date + datetime.timedelta(days=1)
				local_hour = datetime.datetime.strptime("0000", "%H%M")
			else:			
				local_hour = datetime.datetime.strptime(col[ 2], "%H%M")
				
			new_hourly_data['Time'] = local_date + datetime.timedelta(hours=local_hour.hour, minutes=local_hour.minute)
				
			# new_hourly_data['Julian Date'] = col[ 3]
			#print col[ 4]
			new_hourly_data['Reference ETo'] = float(col[ 4])
			# new_hourly_data['QC for Reference ETo'] = col[ 5]
			new_hourly_data['Precipitation'] = float(col[6 ])
			# new_hourly_data['QC for Precipitation'] = col[7 ]
			new_hourly_data['Solar Radiation '] = float(col[8 ])
			# new_hourly_data['QC for Solar Radiation '] = col[9 ]
			new_hourly_data['Vapor Pressure '] = float(col[ 10])
			# new_hourly_data['QC for Vapor Pressure'] = col[11 ]
			new_hourly_data['Air Temperature '] = float(col[12 ])
			# new_hourly_data['QC for Air Temperature'] = col[ 13]
			new_hourly_data['Relative Humidity '] = float(col[ 14])
			# new_hourly_data['QC for Relative Humidity'] = col[ 15]
			new_hourly_data['Dew Point '] = float(col[ 16])
			# new_hourly_data['QC for Dew Point'] = col[ 17]
			new_hourly_data['Wind Speed '] = float(col[ 18])
			# new_hourly_data['QC for Wind Speed'] = col[19 ]
			new_hourly_data['Wind Direction '] = float(col[20 ])
			# new_hourly_data['QC for Wind Direction'] = col[ 21]
			new_hourly_data['Soil Temperature'] = float(col[ 22])
			# new_hourly_data['QC for Soil Temperature'] = col[ 23]
			IrvineWaterData.append(new_hourly_data)		
		
	return IrvineWaterData

def concatIrvineWaterData(data):
	global IrvineWaterDataRaw
	#process data and save it
	IrvineWaterDataRaw = IrvineWaterDataRaw + data
	
def getIrvineWaterData():
	global IrvineWaterDataRaw
	IrvineWaterDataRaw = ''
	#initiate a request data
	ftp = ftplib.FTP("ftpcimis.water.ca.gov")
	ftp.login()
	ftp.cwd("/pub2/hourly")
	file_name = 'hourly075.csv'
	# try:
	ftp.retrbinary('RETR ' + file_name , concatIrvineWaterData)
	ftp.quit()
	return processIrvineWaterData()

#test for this module only, you can use this as an example to call this module from another python module		
if __name__ == "__main__":
	data = getIrvineWaterData()
	pp = pprint.PrettyPrinter(indent=4)
	print pp.pprint(data)





