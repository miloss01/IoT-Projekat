# import RPi.GPIO as GPIO
import time
import random
import json
import paho.mqtt.publish as publish
import threading
from . import constants as c
from datetime import datetime

dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

time_pressed = 0

def generate_values():
  while True:
    now = datetime.now()
    ret = now.strftime('%H:%M')
    yield ret

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

  temp_payload = {
    "measurement": "B4SD",
    "simulated": settings['simulated'],
    "pi": settings["pi"],
    "name": settings["name"],
    "value": value
  }

  with counter_lock:
    dht_batch.append(('B4SD', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Time: {value}")

def run_sensor_simulator(callback, stop_event, settings, event, publish_event):
  for d in generate_values():
    time.sleep(settings["delay"])
    callback(d, settings, event, publish_event)
    if event.is_set():
      print("Room sensor detection event trigger.")
    if stop_event.is_set():
      break

# GPIO.setmode(GPIO.BCM)
 
# # GPIO ports for the 7seg pins
# segments =  (11,4,23,8,7,10,18,25)
# # 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
# for segment in segments:
#     GPIO.setup(segment, GPIO.OUT)
#     GPIO.output(segment, 0)
 
# # GPIO ports for the digit 0-3 pins 
# digits = (22,27,17,24)
# # 7seg_digit_pins (12,9,8,6) digits 0-3 respectively
 
# for digit in digits:
#     GPIO.setup(digit, GPIO.OUT)
#     GPIO.output(digit, 1)
 
# num = {' ':(0,0,0,0,0,0,0),
#     '0':(1,1,1,1,1,1,0),
#     '1':(0,1,1,0,0,0,0),
#     '2':(1,1,0,1,1,0,1),
#     '3':(1,1,1,1,0,0,1),
#     '4':(0,1,1,0,0,1,1),
#     '5':(1,0,1,1,0,1,1),
#     '6':(1,0,1,1,1,1,1),
#     '7':(1,1,1,0,0,0,0),
#     '8':(1,1,1,1,1,1,1),
#     '9':(1,1,1,1,0,1,1)}
 
# try:
#     while True:
#         n = time.ctime()[11:13]+time.ctime()[14:16]
#         s = str(n).rjust(4)
#         for digit in range(4):
#             for loop in range(0,7):
#                 GPIO.output(segments[loop], num[s[digit]][loop])
#                 if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
#                     GPIO.output(25, 1)
#                 else:
#                     GPIO.output(25, 0)
#             GPIO.output(digits[digit], 0)
#             time.sleep(0.001)
#             GPIO.output(digits[digit], 1)
# finally:
#     GPIO.cleanup()
    
def run_b4sd(settings, threads, stop_event, event):
  if settings['simulated']:
    sensor_thread = threading.Thread(target= run_sensor_simulator, args=(sensor_callback, stop_event, settings, event, publish_event))
    sensor_thread.start()
    threads.append(sensor_thread)
    print(f"{settings['name']} simulator started.")
  else:
    print(f"{settings['name']} real started.")