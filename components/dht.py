import threading
import time
import random
import json
import paho.mqtt.publish as publish
# import RPi.GPIO as GPIO

# class DHT(object):
# 	DHTLIB_OK = 0
# 	DHTLIB_ERROR_CHECKSUM = -1
# 	DHTLIB_ERROR_TIMEOUT = -2
# 	DHTLIB_INVALID_VALUE = -999
	
# 	DHTLIB_DHT11_WAKEUP = 0.020#0.018		#18ms
# 	DHTLIB_TIMEOUT = 0.0001			#100us
	
# 	humidity = 0
# 	temperature = 0
	
# 	def __init__(self,pin):
# 		self.pin = pin
# 		self.bits = [0,0,0,0,0]
# 	#Read DHT sensor, store the original data in bits[]	
# 	def readSensor(self,pin,wakeupDelay):
# 		mask = 0x80
# 		idx = 0
# 		self.bits = [0,0,0,0,0]
# 		GPIO.setup(pin,GPIO.OUT)
# 		GPIO.output(pin,GPIO.LOW)
# 		time.sleep(wakeupDelay)
# 		GPIO.output(pin,GPIO.HIGH)
# 		#time.sleep(40*0.000001)
# 		GPIO.setup(pin,GPIO.IN)
		
# 		loopCnt = self.DHTLIB_TIMEOUT
# 		t = time.time()
# 		while(GPIO.input(pin) == GPIO.LOW):
# 			if((time.time() - t) > loopCnt):
# 				#print ("Echo LOW")
# 				return self.DHTLIB_ERROR_TIMEOUT
# 		t = time.time()
# 		while(GPIO.input(pin) == GPIO.HIGH):
# 			if((time.time() - t) > loopCnt):
# 				#print ("Echo HIGH")
# 				return self.DHTLIB_ERROR_TIMEOUT
# 		for i in range(0,40,1):
# 			t = time.time()
# 			while(GPIO.input(pin) == GPIO.LOW):
# 				if((time.time() - t) > loopCnt):
# 					#print ("Data Low %d"%(i))
# 					return self.DHTLIB_ERROR_TIMEOUT
# 			t = time.time()
# 			while(GPIO.input(pin) == GPIO.HIGH):
# 				if((time.time() - t) > loopCnt):
# 					#print ("Data HIGH %d"%(i))
# 					return self.DHTLIB_ERROR_TIMEOUT		
# 			if((time.time() - t) > 0.00005):	
# 				self.bits[idx] |= mask
# 			#print("t : %f"%(time.time()-t))
# 			mask >>= 1
# 			if(mask == 0):
# 				mask = 0x80
# 				idx += 1	
# 		#print (self.bits)
# 		GPIO.setup(pin,GPIO.OUT)
# 		GPIO.output(pin,GPIO.HIGH)
# 		return self.DHTLIB_OK
# 	#Read DHT sensor, analyze the data of temperature and humidity
# 	def readDHT11(self):
# 		rv = self.readSensor(self.pin,self.DHTLIB_DHT11_WAKEUP)
# 		if (rv is not self.DHTLIB_OK):
# 			self.humidity = self.DHTLIB_INVALID_VALUE
# 			self.temperature = self.DHTLIB_INVALID_VALUE
# 			return rv
# 		self.humidity = self.bits[0]
# 		self.temperature = self.bits[2] + self.bits[3]*0.1
# 		sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
# 		if(self.bits[4] is not sumChk):
# 			return self.DHTLIB_ERROR_CHECKSUM
# 		return self.DHTLIB_OK

def parseCheckCode(code):
	if code == 0:
		return "DHTLIB_OK"
	elif code == -1:
		return "DHTLIB_ERROR_CHECKSUM"
	elif code == -2:
		return "DHTLIB_ERROR_TIMEOUT"
	elif code == -999:
		return "DHTLIB_INVALID_VALUE"
	
dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
  global publish_data_counter, publish_data_limit
  while True:
    event.wait()
    with counter_lock:
      local_dht_batch = dht_batch.copy()
      publish_data_counter = 0
      dht_batch.clear()
    publish.multiple(local_dht_batch, hostname="localhost", port=1883)
    print(f'published {publish_data_limit} dht values')
    event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dht_callback(humidity, temperature, settings, publish_event):
  t = time.localtime()
  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Humidity: {humidity}%, Temperature: {temperature}°C")
	
  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "Temperature",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": temperature
  }

  humidity_payload = {
      "measurement": "Humidity",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": humidity
  }

  with counter_lock:
    dht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
    dht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

def generate_values(initial_temp = 25, initial_humidity=20):
  temperature = initial_temp
  humidity = initial_humidity
  while True:
    temperature += random.randint(-1, 1)
    humidity += random.randint(-1, 1)
    if humidity < 0:
      humidity = 0
    if humidity > 100:
      humidity = 100
    yield humidity, temperature

def run_dht_simulator(callback, stop_event, settings, publish_event):
  for h, t in generate_values():
    time.sleep(settings["delay"])
    callback(h, t, settings, publish_event)
    if stop_event.is_set():
      break
		
def run_dht_real(dht, callback, stop_event, publish_event, settings):
  while True:
    check = dht.readDHT11()
    code = parseCheckCode(check)
    humidity, temperature = dht.humidity, dht.temperature
    callback(humidity, temperature, publish_event, settings, code)
    if stop_event.is_set():
        break
    time.sleep(settings["delay"])  # Delay between readings

def run_dht(settings, threads, stop_event):
  if settings['simulated']:
    dht_thread = threading.Thread(target = run_dht_simulator, args=(dht_callback, stop_event, settings, publish_event))
    dht_thread.start()
    threads.append(dht_thread)
    print(f"{settings['name']} simulator started.")
  else:
    # dht = DHT(settings['pin'])
    dht = None
    dht_thread = threading.Thread(target = run_dht_real, args=(dht, dht_callback, stop_event, publish_event, settings))
    dht_thread.start()
    threads.append(dht_thread)
    print(f"{settings['name']} simulator started.")