import threading
import time
import random

def uds_callback(distance, code):
  t = time.localtime()
  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Distance: {distance}cm")

def generate_values(initial_distance = 25):
  distance = initial_distance
  while True:
    distance += random.randint(-10, 10)
    yield distance

def run_uds_simulator(delay, callback, stop_event, code):
  for d in generate_values():
    time.sleep(delay)
    callback(d, code)
    if stop_event.is_set():
      break

def run_uds(settings, threads, stop_event, code):
  if settings['simulated']:
    uds_thread = threading.Thread(target = run_uds_simulator, args=(settings["delay"], uds_callback, stop_event, code))
    uds_thread.start()
    threads.append(uds_thread)
    print(f"{code} simulator started.")