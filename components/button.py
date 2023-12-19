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


def generate_values(initial_detection = False):
  detection = initial_detection
  while True:
    detection = random.randint(1, 6)
    yield detection


def publisher_task(event, dht_batch):
  global publish_data_counter, publish_data_limit
  while True:
    event.wait()
    with counter_lock:
      local_dht_batch = dht_batch.copy()
      publish_data_counter = 0
      dht_batch.clear()
    publish.multiple(local_dht_batch, hostname="localhost", port=1883)
    print(f'published {publish_data_limit} sensor readings')
    event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def sensor_callback(sensor_hold_value, settings, event, publish_event):
  t = time.localtime()

  global publish_data_counter, publish_data_limit, publish_data_limit

  temp_payload = {
    "measurement": "SensorHoldTime",
    "simulated": settings['simulated'],
    "pi": settings["pi"],
    "name": settings["name"],
    "value": sensor_hold_value
  }

  with counter_lock:
    dht_batch.append(('DS1', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, Button clicked.")

def run_sensor_simulator(callback, stop_event, settings, event, publish_event):
  for d in generate_values():
    time.sleep(settings["delay"])
    callback(d, settings, event, publish_event)
    if event.is_set():
      print("Room sensor detection event trigger.")
    if stop_event.is_set():
      break



# def button_pressed(callback, settings, event, publish_event):
#   button_pressed_time = 0
#   button_pressed = time.time()
#
#   try:
#     while True:
#       if GPIO.input(settings["port_button"]) == GPIO.LOW:
#
#         current_time = time.time()
#         duration = current_time - button_pressed_time
#         callback(duration, settings, event, publish_event)
#         print(f"Button held for {duration:.2f} seconds")
#       else:
#         button_pressed_time = 0
#       time.sleep(0.1)  # Add a small delay to avoid excessive checking
#
#   except KeyboardInterrupt:
#     GPIO.cleanup()
#
# def run_button_real(callback, stop_event, settings, event, publish_event):
#   port_button = settings["port_button"]
#   GPIO.setmode(GPIO.BCM)
#   GPIO.setup(port_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#   GPIO.add_event_detect(port_button, GPIO.RISING, callback = button_pressed(callback, settings, event, publish_event), bouncetime = 100)

def run_button(settings, threads, stop_event, event):
  if settings['simulated']:
    sensor_thread = threading.Thread(target= run_sensor_simulator, args=(sensor_callback, stop_event, settings, event, publish_event))
    sensor_thread.start()
    threads.append(sensor_thread)
    print(f"{settings['name']} simulator started.")
    #run_button_simulator(settings)
  else:
  #   run_button_real(settings)
  #   sensor_thread = threading.Thread(target=run_button_real, args=(sensor_callback, stop_event, settings, event, publish_event))
  #   sensor_thread.start()
  #   threads.append(sensor_thread)
    print(f"{settings['name']} real started.")
