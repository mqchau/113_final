#importimport RPi.GPIO as GPIOimport timeimport os# Define GPIO to LCD mappingLCD_RS = 7LCD_E  = 8LCD_D4 = 25 LCD_D5 = 24LCD_D6 = 23LCD_D7 = 18#LEDLED = 4############################################################# THERMISTOR STUFF #############################################################DEBUG = 1# change these as desired - they're the pins connected from the# SPI port on the ADC to the CobblerSPICLK = 18SPIMISO = 22SPIMOSI = 27SPICS = 17def initializePeripheral():	# set up the SPI interface pins	GPIO.setup(SPIMOSI, GPIO.OUT)	GPIO.setup(SPIMISO, GPIO.IN)	GPIO.setup(SPICLK, GPIO.OUT)	GPIO.setup(SPICS, GPIO.OUT)	GPIO.setup(LED, GPIO.OUT)	GPIO.setup(LCD_E, GPIO.OUT)  # E	GPIO.setup(LCD_RS, GPIO.OUT) # RS	GPIO.setup(LCD_D4, GPIO.OUT) # DB4	GPIO.setup(LCD_D5, GPIO.OUT) # DB5	GPIO.setup(LCD_D6, GPIO.OUT) # DB6	GPIO.setup(LCD_D7, GPIO.OUT) # DB7# 10k trim pot connected to adc #0SensorPortDict = dict()SensorPortDict[0] = "thermistor"max_device_count = 1current_device = 0			#default device to read############################################################# THERMISTOR STUFF ############################################################## Define some device constantsLCD_WIDTH = 16    # Maximum characters per lineLCD_CHR = TrueLCD_CMD = FalseLCD_LINE_1 = 0x80 # LCD RAM address for the 1st lineLCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line # Timing constantsE_PULSE = 0.00005E_DELAY = 0.00005def lcd_run():  # Main program block  #GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers  # Initialise display  lcd_init()  # Send some test  lcd_byte(LCD_LINE_1, LCD_CMD)  lcd_string("irrigation")  lcd_byte(LCD_LINE_2, LCD_CMD)  lcd_string("team 9")  time.sleep(3) # 3 second delay  # Send some text  lcd_byte(LCD_LINE_1, LCD_CMD)  lcd_string("7250 sq ft")  lcd_byte(LCD_LINE_2, LCD_CMD)  lcd_string("two section")  time.sleep(2)'''You only need to use following 4 functions to control LCD'''def lcd_init():  # Initialise display  lcd_byte(0x33,LCD_CMD)  lcd_byte(0x32,LCD_CMD)  lcd_byte(0x28,LCD_CMD)  lcd_byte(0x0C,LCD_CMD)    lcd_byte(0x06,LCD_CMD)  lcd_byte(0x01,LCD_CMD)  def lcd_write_top(message):	lcd_byte(LCD_LINE_1, LCD_CMD)	lcd_string(message)def lcd_write_bottom(message):	lcd_byte(LCD_LINE_2, LCD_CMD)	lcd_string(message)def lcd_clear():	lcd_write_top("")	lcd_write_bottom("")'''End of public APIs of LCD'''def lcd_string(message):  # Send string to display  message = message.ljust(LCD_WIDTH," ")    for i in range(LCD_WIDTH):    lcd_byte(ord(message[i]),LCD_CHR)def lcd_byte(bits, mode):  # Send byte to data pins  # bits = data  # mode = True  for character  #        False for command  GPIO.output(LCD_RS, mode) # RS  # High bits  GPIO.output(LCD_D4, False)  GPIO.output(LCD_D5, False)  GPIO.output(LCD_D6, False)  GPIO.output(LCD_D7, False)  if bits&0x10==0x10:    GPIO.output(LCD_D4, True)  if bits&0x20==0x20:    GPIO.output(LCD_D5, True)  if bits&0x40==0x40:    GPIO.output(LCD_D6, True)  if bits&0x80==0x80:    GPIO.output(LCD_D7, True)  # Toggle 'Enable' pin  time.sleep(E_DELAY)      GPIO.output(LCD_E, True)    time.sleep(E_PULSE)  GPIO.output(LCD_E, False)    time.sleep(E_DELAY)        # Low bits  GPIO.output(LCD_D4, False)  GPIO.output(LCD_D5, False)  GPIO.output(LCD_D6, False)  GPIO.output(LCD_D7, False)  if bits&0x01==0x01:    GPIO.output(LCD_D4, True)  if bits&0x02==0x02:    GPIO.output(LCD_D5, True)  if bits&0x04==0x04:    GPIO.output(LCD_D6, True)  if bits&0x08==0x08:    GPIO.output(LCD_D7, True)  # Toggle 'Enable' pin  time.sleep(E_DELAY)      GPIO.output(LCD_E, True)    time.sleep(E_PULSE)  GPIO.output(LCD_E, False)    time.sleep(E_DELAY)    ############################################################# THERMISTOR STUFF ############################################################## read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)def readadc(adcnum, clockpin, mosipin, misopin, cspin):    if ((adcnum > 7) or (adcnum < 0)):        return -1    GPIO.output(cspin, True)        GPIO.output(clockpin, False)  # start clock low    GPIO.output(cspin, False)     # bring CS low        commandout = adcnum    commandout |= 0x18  # start bit + single-ended bit    commandout <<= 3    # we only need to send 5 bits here    for i in range(5):        if (commandout & 0x80):            GPIO.output(mosipin, True)        else:            GPIO.output(mosipin, False)        commandout <<= 1        GPIO.output(clockpin, True)        GPIO.output(clockpin, False)        adcout = 0    # read in one empty bit, one null bit and 10 ADC bits    for i in range(12):        GPIO.output(clockpin, True)        GPIO.output(clockpin, False)        adcout <<= 1        if (GPIO.input(misopin)):            adcout |= 0x1        GPIO.output(cspin, True)        adcout >>= 1       # first bit is 'null' so drop it    return adcout	def display_thermistor():	for i in range(5):		#read from current device		current_value = readadc(current_device, SPICLK, SPIMOSI, SPIMISO, SPICS)				#display reading		#print(SensorPortDict[current_device] + " has value = " + str(current_value))		time.sleep(1)		print "current temp = " + str(calculate_temperature(current_value)) + "F"	def calculate_temperature(displayValue):	Resistance = 10000 * 1024 / float(displayValue) - 10000	Resistance = Resistance * 10 / 3.3	#Resistance = 10000 / float(((1023 / float(displayValue)) - 1))	temperature = 77 - ((Resistance - 10000) / 550)	#print("resistance has value = " + str(Resistance))	#print("temperature has value = " + str(temperature))	return round(temperature, 2)def get_current_temp():	return calculate_temperature(readadc(current_device, SPICLK, SPIMOSI, SPIMISO, SPICS))	############################################################# THERMISTOR STUFF ########################################################################################################################## LED STUFF #############################################################def set_pin_high(gpioNum):	GPIO.output(gpioNum, True)def set_pin_low(gpioNum):	GPIO.output(gpioNum, False)	def flash(delayTime):	for i in range(5):		set_pin_high(LED)		time.sleep(delayTime)		set_pin_low(LED)		time.sleep(delayTime)		def turnOffLED():	set_pin_low(LED)	def turnOnLED():	set_pin_low(LED)	############################################################# LED STUFF #############################################################if __name__ == '__main__':	GPIO.setmode(GPIO.BCM)	initializePeripheral()		lcd_init()	for i in xrange(0, 10):		lcd_write_top("T = " + str(get_current_temp()))		lcd_write_bottom("i = " + str(i))		time.sleep(0.5)	#lcd_write_top('My name is Christ')	#lcd_write_bottom('No you not Christ')	#lcd_run()	#display_thermistor()	flash(1.0)	lcd_clear()		