import threading
import time
import random
import json
import paho.mqtt.publish as publish
from . import constants as c
from . import led as l
# import RPi.GPIO as GPIO

def generate_values(initial_detection = False):
  detection = initial_detection
  while True:
    detection = random.randint(0, 1) < 0.5
    yield detection

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
    print(f'published {publish_data_limit} pir values')
    event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def pir_callback(detected, settings, led_settings, event, publish_event):
  t = time.localtime()

  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "MotionDetection",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": 1 if detected else 0
  }

  with counter_lock:
    dht_batch.append(('PIR', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  if detected:
    l.run_led(led_settings)
    event.set()
  else:
    event.clear()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Motion detected: {detected}")

def run_pir_simulator(callback, stop_event, settings, led_settings, event, publish_event):
  for d in generate_values():
    time.sleep(settings["delay"])
    callback(d, settings, led_settings, event, publish_event)
    if event.is_set():
      print("Motion detection event trigger.")
    if stop_event.is_set():
      break

def run_pir(settings, led_settings, threads, stop_event, event):
  if settings['simulated']:
    pir_thread = threading.Thread(target = run_pir_simulator, args=(pir_callback, stop_event, settings, led_settings, event, publish_event))
    pir_thread.start()
    threads.append(pir_thread)
    print(f"{settings['name']} simulator started.")
  else:
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings["pin"], GPIO.IN)
    # GPIO.add_event_detect(settings["pin"], GPIO.RISING, callback=lambda x: pir_callback(True, settings, led_settings, event, publish_event))
    # # GPIO.add_event_detect(settings["pin"], GPIO.FALLING, callback=lambda x: pir_callback(False, settings, led_settings, event, publish_event))
    print(f"{settings['name']} real started.")
