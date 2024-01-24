import threading
import time
import random
import json
import paho.mqtt.publish as publish
from . import constants as c
# import RPi.GPIO as GPIO

dht_batch = []
publish_data_counter = 0
publish_data_limit = 1
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
    print(f'published {publish_data_limit} led values')
    event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_led_simulator(settings):
  t = time.localtime()

  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "light",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": "on"
  }

  with counter_lock:
    dht_batch.append(('LED', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, is turned on")

  time.sleep(settings["duration"])

  temp_payload["value"] = "off"

  with counter_lock:
    dht_batch.append(('LED', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, is turned off")

def run_led_real(settings):
  t = time.localtime()

  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "light",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": "on"
  }

  with counter_lock:
    dht_batch.append(('LED', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  # GPIO.output(settings["pin"], GPIO.HIGH)
  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, is turned on")
  time.sleep(settings["duration"])
  # GPIO.output(settings["pin"], GPIO.LOW)
  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, is turned off")

def run_led(settings):
  if settings['simulated']:
    run_led_simulator(settings)
  else:
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings['pin'], GPIO.OUT)
    run_led_real(settings)