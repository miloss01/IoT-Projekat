import time
import random
import json
import paho.mqtt.publish as publish
import threading

#import RPi.GPIO as GPIO
import time

# these GPIO pins are connected to the keypad
# change these according to your connections!
R1 = 25
R2 = 8
R3 = 7
R4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Initialize the GPIO pins
#
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(R1, GPIO.OUT)
# GPIO.setup(R2, GPIO.OUT)
# GPIO.setup(R3, GPIO.OUT)
# GPIO.setup(R4, GPIO.OUT)
#
# # Make sure to configure the input pins to use the internal pull-down resistors
#
# GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#
# def readLine(line, characters):
#   GPIO.output(line, GPIO.HIGH)
#   pressed_character = None
#
#   if GPIO.input(C1) == 1:
#     pressed_character = characters[0]
#   elif GPIO.input(C2) == 1:
#     pressed_character = characters[1]
#   elif GPIO.input(C3) == 1:
#     pressed_character = characters[2]
#   elif GPIO.input(C4) == 1:
#     pressed_character = characters[3]
#
#   GPIO.output(line, GPIO.LOW)
#   return pressed_character

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
  dms_input = ""
  while True:
    value = ""
    print("")
    print("Current input: " + dms_input)
    print("X - Submit input")
    print("C - Cancel writing")

    # if(settings['simulated']):
    #   pressed_key = None
    #   while pressed_key is None:
    #     for row, chars in zip([R1, R2, R3, R4], [["1", "2", "3", "A"], ["4", "5", "6", "B"],
    #                                              ["7", "8", "9", "C"], ["*", "0", "#", "D"]]):
    #       pressed_key = readLine(row, chars)
    #       if pressed_key is not None:
    #         break
    #     time.sleep(0.2)
    #   value = pressed_key
    # else: U OVAJ ELSE IDE VALUE = INPUT("ENTER CHARACTER: ")
    value = input("Enter character: ")

    if value == "X" and len(dms_input) != 0:
      print("SUBMITTED VALUE: " + dms_input)
      run_keypad_simulator(settings, dms_input)
      dms_input = ""
      continue
    if value == "C":
      break
    if (value.isdigit() or value in ['*','#','A','B','C','D'] ) and len(value) == 1:
      dms_input += value
    else:
      print("You must input one character number")


