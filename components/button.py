import time
import random
import json
import paho.mqtt.publish as publish
import threading
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
    publish.multiple(local_dht_batch, hostname="localhost", port=1883)
    print(f'published {publish_data_limit} button clicks')
    event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def run_button_simulator(settings):
  t = time.localtime()

  global publish_data_counter, publish_data_limit, publish_data_limit

  temp_payload = {
    "measurement": "button hold time",
    "simulated": settings['simulated'],
    "pi": settings["pi"],
    "name": settings["name"],
    "value": random.randrange(1, 6)
  }

  with counter_lock:
    dht_batch.append(('DS1', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Button clicked.")

# def run_button_real(settings):
#   port_button = settings["port_button"]
#   GPIO.setmode(GPIO.BCM)
#   GPIO.setup(port_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#   GPIO.add_event_detect(port_button, GPIO.RISING, callback = button_pressed, bouncetime = 100)

def run_button(settings):
  if settings['simulated']:
    run_button_simulator(settings)
  # else:
  #   run_button_real(settings)
