#!/usr/bin/env python3
# import MPU6050 
import time
import random
import os
import json
import paho.mqtt.publish as publish
import threading
from . import constants as c

dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

time_pressed = 0

def generate_values():
  while True:
    x, y, z = random.uniform(0.001, 2), random.uniform(0.001, 2), random.uniform(0.001, 2)
    ret = f"{str(x)}:{str(y)}:{str(z)}"
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
    "measurement": "Rotation",
    "simulated": settings['simulated'],
    "pi": settings["pi"],
    "name": settings["name"],
    "value": value
  }

  with counter_lock:
    dht_batch.append(('GYRO', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Value {value}.")

def run_sensor_simulator(callback, stop_event, settings, event, publish_event):
  for d in generate_values():
    time.sleep(settings["delay"])

    callback(d, settings, event, publish_event)

    if event.is_set():
      print("Room sensor detection event trigger.")
    if stop_event.is_set():
      break

# mpu = MPU6050.MPU6050()     #instantiate a MPU6050 class object
# accel = [0]*3               #store accelerometer data
# gyro = [0]*3                #store gyroscope data
# def setup():
#     mpu.dmp_initialize()    #initialize MPU6050
    
# def loop():
#     while(True):
#         accel = mpu.get_acceleration()      #get accelerometer data
#         gyro = mpu.get_rotation()           #get gyroscope data
#         os.system('clear')
#         print("a/g:%d\t%d\t%d\t%d\t%d\t%d "%(accel[0],accel[1],accel[2],gyro[0],gyro[1],gyro[2]))
#         print("a/g:%.2f g\t%.2f g\t%.2f g\t%.2f d/s\t%.2f d/s\t%.2f d/s"%(accel[0]/16384.0,accel[1]/16384.0,
#             accel[2]/16384.0,gyro[0]/131.0,gyro[1]/131.0,gyro[2]/131.0))
#         time.sleep(0.1)
        
# if __name__ == '__main__':     # Program start from here
#     print("Program is starting ... ")
#     setup()
#     try:
#         loop()
#     except KeyboardInterrupt:  # When 'Ctrl+C' is pressed,the program will exit.
#         pass

def run_gyro(settings, threads, stop_event, event):
    if settings['simulated']:
        sensor_thread = threading.Thread(target= run_sensor_simulator, args=(sensor_callback, stop_event, settings, event, publish_event))
        sensor_thread.start()
        threads.append(sensor_thread)
        print(f"{settings['name']} simulator started.")

