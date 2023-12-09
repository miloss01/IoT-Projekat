import threading
import time
import random
import json
import paho.mqtt.publish as publish

def dht_callback(humidity, temperature, code):
  t = time.localtime()
  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Humidity: {humidity}%, Temperature: {temperature}°C")
  batch = []
  payload = {
    "measurement": "some measurement",
    "some_tag": "tag  " + str(random.randint(1, 100)),
    "some_field": "field" + str(random.randint(1, 100))
  }
  batch.append(('example_topic', json.dumps(payload), 0, True))
  publish.multiple(batch, hostname="localhost", port=1883)

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

def run_dht_simulator(delay, callback, stop_event, code):
  for h, t in generate_values():
    time.sleep(delay)
    callback(h, t, code)
    if stop_event.is_set():
      break

def run_dht(settings, threads, stop_event, code):
  if settings['simulated']:
    dht_thread = threading.Thread(target = run_dht_simulator, args=(settings["delay"], dht_callback, stop_event, code))
    dht_thread.start()
    threads.append(dht_thread)
    print(f"{code} simulator started.")