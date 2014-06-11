
import GetIrvinePrecipitation, datetime, re
import HTML

def UpdateHTML(time_string, current_temp, duration, schedule, data_table):
	new_html_code = "";

	file = open("skeleton.html", "r")
	line = file.readline()
	while line:
		if re.search("Put current virtual time here", line):
			#put the time here
			new_html_code = new_html_code + time_string + "<br>\n"
			new_html_code = new_html_code + "Current temperature is " + str(current_temp) + " degree F<br>\n"
		elif re.search("Put water duration and time to water", line):
			#put the duration + schedule
			new_html_code = new_html_code + "Water duration is " + str(duration) + " minutes<br>\n"
			new_html_code = new_html_code + "The time to water is at " 
			
			if len(schedule) > 1:
				for counter in xrange(len(schedule)):				
					if counter < len(schedule) - 1:
						new_html_code = new_html_code + str(schedule[counter]) + ":00, "
					else:
						new_html_code = new_html_code + "and " + str(schedule[counter]) + ":00"
			else:
				new_html_code = new_html_code + str(schedule[0]) + ":00"
					
			new_html_code = new_html_code + "<br>\n"
		elif re.search("Put table of hourly data here", line):
			#put hourly precipitation here
			table_data = list()
			#first row for information:
			first_row = ['Time', 'Reference ETo (in)', 'Precipitation (in)', 'Solar Radiation (Ly/day)', 'Vapor Pressure (mBars)', 'Air Temperature (F)', 'Relative Humidity (%)', 'Dew Point (F)', 'Wind Speed (MPH)', 'Wind Direction ', 'Soil Temperature (F)']
			table_data.append(first_row)
			
			#start data
			for new_hourly_data in data_table:
				new_row = list()
				new_row.append(str(new_hourly_data['Time'])	)			
				new_row.append(str(new_hourly_data['Reference ETo'] ))
				
				new_row.append(str(new_hourly_data['Precipitation'] ))
				
				new_row.append(str(new_hourly_data['Solar Radiation '] ))
				
				new_row.append(str(new_hourly_data['Vapor Pressure '] ))
				
				new_row.append(str(new_hourly_data['Air Temperature '] ))
				
				new_row.append(str(new_hourly_data['Relative Humidity '] ))
				
				new_row.append(str(new_hourly_data['Dew Point '] ))
				
				new_row.append(str(new_hourly_data['Wind Speed '] ))
				
				new_row.append(str(new_hourly_data['Wind Direction '] ))
				
				new_row.append(str(new_hourly_data['Soil Temperature'] ))
				
			
				table_data.append(new_row)
			
			# new_row.append(new_hourly_data['Reference ETo'] = float(col[ 4])
			# # new_row.append(new_hourly_data['QC for Reference ETo'] = col[ 5]
			# new_row.append(new_hourly_data['Precipitation'] = float(col[6 ])
			# # new_row.append(new_hourly_data['QC for Precipitation'] = col[7 ]
			# new_row.append(new_hourly_data['Solar Radiation '] = float(col[8 ])
			# # new_row.append(new_hourly_data['QC for Solar Radiation '] = col[9 ]
			# new_row.append(new_hourly_data['Vapor Pressure '] = float(col[ 10])
			# # new_row.append(new_hourly_data['QC for Vapor Pressure'] = col[11 ]
			# new_row.append(new_hourly_data['Air Temperature '] = float(col[12 ])
			# # new_row.append(new_hourly_data['QC for Air Temperature'] = col[ 13]
			# new_row.append(new_hourly_data['Relative Humidity '] = float(col[ 14])
			# # new_row.append(new_hourly_data['QC for Relative Humidity'] = col[ 15]
			# new_row.append(new_hourly_data['Dew Point '] = float(col[ 16])
			# # new_row.append(new_hourly_data['QC for Dew Point'] = col[ 17]
			# new_row.append(new_hourly_data['Wind Speed '] = float(col[ 18])
			# # new_row.append(new_hourly_data['QC for Wind Speed'] = col[19 ]
			# new_row.append(new_hourly_data['Wind Direction '] = float(col[20 ])
			# # new_row.append(new_hourly_data['QC for Wind Direction'] = col[ 21]
			# new_row.append(new_hourly_data['Soil Temperature'] = float(col[ 22])
			# # new_row.append(new_hourly_data['QC for Soil Temperature'] = col[ 23]
			
			
				[
				['Last name',   'First name',   'Age'],
				['Smith',       'John',         30],
				['Carpenter',   'Jack',         47],
				['Johnson',     'Paul',         62],
			]
			new_html_code = new_html_code + "\n" + HTML.table(table_data) + "\n"
		
		else:
			new_html_code = new_html_code + line
		
		line = file.readline()
	file.close()
	
	#write to new file
	file = open("index.html", "w")
	file.truncate()
	file.write(new_html_code)
	file.close()
			



if "__main__" == __name__:

	UpdateHTML(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), 73.4, 1.2, [20], GetIrvinePrecipitation.getIrvineWaterData())

