import threading
import time
import random

def pir_callback(detected, code, event):
  t = time.localtime()

  if detected:
    event.set()
  else:
    event.clear()

  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Motion detected: {detected}")

def generate_values(initial_detection = False):
  detection = initial_detection
  while True:
    detection = random.randint(0, 1) < 0.5
    yield detection

def run_pir_simulator(delay, callback, stop_event, code, event):
  for d in generate_values():
    time.sleep(delay)
    callback(d, code, event)
    if event.is_set():
      print("Nesto")
    if stop_event.is_set():
      break

def run_pir(settings, threads, stop_event, code, event):
  if settings['simulated']:
    pir_thread = threading.Thread(target = run_pir_simulator, args=(settings["delay"], pir_callback, stop_event, code, event))
    pir_thread.start()
    threads.append(pir_thread)
    print(f"{code} simulator started.")