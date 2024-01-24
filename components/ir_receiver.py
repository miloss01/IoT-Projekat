#-----------------------------------------#
# Name - IR-Finalized.py
# Description - The finalized code to read data from an IR sensor and then reference it with stored values
# Author - Lime Parallelogram
# License - Completely Free
# Date - 12/09/2019
#------------------------------------------------------------#
# Imports modules
# import RPi.GPIO as GPIO
from datetime import datetime
import time
import random
import json
import paho.mqtt.publish as publish
import threading
from . import constants as c

dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

r = 0
g = 0
b = 0

def set_rgb(rgb):
  global r, g, b
  tokens = rgb.split(":")
  r = int(tokens[0])
  g = int(tokens[1])
  b = int(tokens[2])

def generate_values():
  while True:
    r, g, b = random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)
    yield (r, g, b)


def publisher_task(event, dht_batch):
  global publish_data_counter, publish_data_limit
  while True:
    event.wait()
    with counter_lock:
      local_dht_batch = dht_batch.copy()
      publish_data_counter = 0
      dht_batch.clear()
    publish.multiple(local_dht_batch, hostname=c.MQTT_HOSTNAME, port=c.MQTT_PORT)
    print(f'published {publish_data_limit} sensor readings')
    event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def sensor_callback(value, settings, event, publish_event):
  t = time.localtime()

  global publish_data_counter, publish_data_limit, publish_data_limit
  global r, g, b
  r = value[0]
  g = value[1]
  b = value[2]
  value_str = f"{r}:{g}:{b}"
  
  temp_payload = {
    "measurement": "color",
    "simulated": settings['simulated'],
    "pi": settings["pi"],
    "name": settings["name"],
    "value": value_str
  }
	
  with counter_lock:
    dht_batch.append(('BIR', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, BIR: {value_str}.")

def run_sensor_simulator(callback, stop_event, settings, event, publish_event):
  for d in generate_values():
    time.sleep(settings["delay"])
    
    callback(d, settings, event, publish_event)
    
    if event.is_set():
      print("Room sensor detection event trigger.")
    if stop_event.is_set():
      break

# Static program vars
pin = 17
Buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5, 0x300ff52ad]  # HEX code list
ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",          "1",        "OK",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list

# Sets up GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin, GPIO.IN)

# Gets binary value


def getBinary():
	pass
	# Internal vars
	# num1s = 0  # Number of consecutive 1s read
	# binary = 1  # The binary value
	# command = []  # The list to store pulse times in
	# previousValue = 0  # The last value
	# value = GPIO.input(pin)  # The current value

	# # Waits for the sensor to pull pin low
	# while value:
	# 	time.sleep(0.0001) # This sleep decreases CPU utilization immensely
	# 	value = GPIO.input(pin)
		
	# # Records start time
	# startTime = datetime.now()
	
	# while True:
	# 	# If change detected in value
	# 	if previousValue != value:
	# 		now = datetime.now()
	# 		pulseTime = now - startTime #Calculate the time of pulse
	# 		startTime = now #Reset start time
	# 		command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
	# 	# Updates consecutive 1s variable
	# 	if value:
	# 		num1s += 1
	# 	else:
	# 		num1s = 0
		
	# 	# Breaks program when the amount of 1s surpasses 10000
	# 	if num1s > 10000:
	# 		break
			
	# 	# Re-reads pin
	# 	previousValue = value
	# 	value = GPIO.input(pin)
		
	# # Converts times to binary
	# for (typ, tme) in command:
	# 	if typ == 1: #If looking at rest period
	# 		if tme > 1000: #If pulse greater than 1000us
	# 			binary = binary *10 +1 #Must be 1
	# 		else:
	# 			binary *= 10 #Must be 0
			
	# if len(str(binary)) > 34: #Sometimes, there is some stray characters
	# 	binary = int(str(binary)[:34])
		
	# return binary
	
# Convert value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
	return hex(tmpB2)
	
# while True:
# 	inData = convertHex(getBinary()) #Runs subs to get incoming hex value
# 	for button in range(len(Buttons)):#Runs through every value in list
# 		if hex(Buttons[button]) == inData: #Checks this against incoming
# 			print(ButtonsNames[button]) #Prints corresponding english name for button

def run_ir(settings, threads, stop_event, event):
  if settings['simulated']:
    rgb_thread = threading.Thread(target= run_sensor_simulator, args=(sensor_callback, stop_event, settings, event, publish_event))
    rgb_thread.start()
    threads.append(rgb_thread)
    print(f"{settings['name']} simulator started.")