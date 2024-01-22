#!/usr/bin/env python3

# from PCF8574 import PCF8574_GPIO
# from Adafruit_LCD1602 import Adafruit_CharLCD
from . import Adafruit_LCD1602 as ada
from . import PCF8574 as pcf

from time import sleep, strftime
from datetime import datetime

text = "T-0 H-0"
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')
    
def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
        #lcd.clear()
        global text
        lcd.setCursor(0,0)  # set cursor position
        # lcd.message( 'CPU: ' + get_cpu_temp()+'\n' )# display CPU temperature
        # lcd.message( get_time_now() )   # display the time
        lcd.message(text)
        sleep(1)
        
def destroy():
    lcd.clear()

def set_text(t):
    global text
    tokens = text.split(" ")

    if t[0] == "T":
        text = t + " " + tokens[1]
    if t[0] == "H":
        text = tokens[0] + " " + t
    
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = pcf.PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = pcf.PCF8574_GPIO(PCF8574A_address)
	except:
		print ('I2C Address Error !')
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = ada.Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

