import threading
import time
import random
import json
import paho.mqtt.publish as publish
from . import constants as c

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
    print(f'published {publish_data_limit} buzz values')
    event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def run_buzz_simulator(settings):
  t = time.localtime()

  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "buzz",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": 1
  }

  with counter_lock:
    dht_batch.append(('Buzz', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Buzzzzz")

def buzz(pitch, duration, buzzer_pin):
  period = 1.0 / pitch
  delay = period / 2
  cycles = int(duration * pitch)
  for i in range(cycles):
    # GPIO.output(buzzer_pin, True)
    time.sleep(delay)
    # GPIO.output(buzzer_pin, False)
    time.sleep(delay)


def run_buzz_real(settings):
  t = time.localtime()

  pitch = 440
  duration = 0.1
  buzz(pitch, duration, settings["pin"])

  global publish_data_counter, publish_data_limit

  temp_payload = {
      "measurement": "buzz",
      "simulated": settings['simulated'],
      "pi": settings["pi"],
      "name": settings["name"],
      "value": 1
  }

  with counter_lock:
    dht_batch.append(('Buzz', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Buzzzzz")

def run_buzz(settings):
  if settings['simulated']:
    run_buzz_simulator(settings)
  else:
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(settings['pin'], GPIO.OUT)
    run_buzz_real(settings)