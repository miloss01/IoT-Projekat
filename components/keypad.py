import time
import random
import json
import paho.mqtt.publish as publish
import threading

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
    print(f'published {publish_data_limit} DMS input')
    event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def run_keypad_simulator(settings, dms_input):
  t = time.localtime()

  global publish_data_counter, publish_data_limit, publish_data_limit

  temp_payload = {
    "measurement": "DMSInputValue",
    "simulated": settings['simulated'],
    "pi": settings["pi"],
    "name": settings["name"],
    "value": dms_input
  }

  with counter_lock:
    dht_batch.append(('DMS', json.dumps(temp_payload), 0, True))
    publish_data_counter += 1

  #OVDE IMA 5 ENTRIJA ALI U BAZI UPISE 6 ZASTOOOO
  print(dht_batch)
  if publish_data_counter >= publish_data_limit:
    publish_event.set()

  print(f"Code: {settings['name']}, Timestamp: {time.strftime('%H:%M:%S', t)}, DMS input value: {dms_input}.")
def run_keypad(settings):
  if settings['simulated']:
    dms_input = ""
    while True:
      value = ""
      print("")
      print("Current input: " + dms_input)
      print("X - Submit input")
      print("C - Cancel writing")
      value = input("Enter number: ")
      if value == "X" and len(dms_input) != 0:
        print("SUBMITTED VALUE: " + dms_input)
        run_keypad_simulator(settings, dms_input)
        dms_input = ""
        continue
      if value == "C":
        break
      if value.isdigit() and len(value) == 1:
        dms_input += value
      else:
        print("You must input one character number")
