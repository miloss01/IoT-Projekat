import threading
import time
import random
import json
import paho.mqtt.publish as publish
from . import constants as c
# import RPi.GPIO as GPIO

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
    publish.multiple(local_dht_batch, hostname=c.MQTT_HOSTNAME, port=c.MQTT_PORT)
    print(f'published {publish_data_limit} uds values')
    event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

# def get_distance(trig, echo):
#   GPIO.output(trig, False)
#   time.sleep(0.2)
#   GPIO.output(trig, True)
#   time.sleep(0.00001)
#   GPIO.output(trig, False)
#   pulse_start_time = time.time()
#   pulse_end_time = time.time()

#   max_iter = 100

#   iter = 0
#   while GPIO.input(echo) == 0:
#       if iter > max_iter:
#           return None
#       pulse_start_time = time.time()
#       iter += 1

#   iter = 0
#   while GPIO.input(echo) == 1:
#       if iter > max_iter:
#           return None
#       pulse_end_time = time.time()
#       iter += 1

#   pulse_duration = pulse_end_time - pulse_start_time
#   distance = (pulse_duration * 34300)/2
#   return distance

def generate_values(initial_distance = 25):
  distance = initial_distance
  while True:
    distance += random.randint(-10, 10)
    yield distance

def uds_callback(distance, settings):
  t = time.localtime()

  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "Distance",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": distance
  }

  with counter_lock:
    dht_batch.append(('UDS', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Distance: {distance}cm")


def run_uds_simulator(settings, callback, stop_event):
  for d in generate_values():
    time.sleep(settings["delay"])
    callback(d, settings)
    if stop_event.is_set():
      break

def run_uds_real(settings, callback, stop_event):
  while True:
    if stop_event.is_set():
      break
    # distance = get_distance(settings["trig"], settings["echo"])
    distance = None
    if distance is not None:
      callback(distance, settings)

def run_uds(settings, threads, stop_event):
  if settings['simulated']:
    uds_thread = threading.Thread(target = run_uds_simulator, args=(settings, uds_callback, stop_event))
    uds_thread.start()
    threads.append(uds_thread)
    print(f"{settings['name']} simulator started.")
  else:
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings["trig"], GPIO.OUT)
    # GPIO.setup(settings["echo"], GPIO.IN)
    uds_thread = threading.Thread(target = run_uds_real, args=(settings, uds_callback, stop_event))
    uds_thread.start()
    threads.append(uds_thread)
    print(f"{settings['name']} real started.")