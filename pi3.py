
import threading
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.led import run_led
from components.buzz import run_buzz
from components.keypad import run_keypad
from components.b4sd import run_b4sd
import time

# try:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)
# except:
#     pass

def menu(settings):
  print("1 - DMS - Door Membrane Switch")
  print("2 - DL - Door Light")
  print("3 - DB - Door Buzzer")
  print("X - Exit")

  dl_settings = settings['DL']
  db_settings = settings['DB']
  dms_settings = settings['DMS']

  while True:
    option = input("")
    if option == "X":
      break
    if option == "1":
      run_keypad(dms_settings)
    if option == "2":
      run_led(dl_settings)
    if option == "3":
      run_buzz(db_settings)



if __name__ == "__main__":
  print('Starting app')

  settings = load_settings()
  threads = []
  stop_event = threading.Event()

  rpir4_event = threading.Event()
  sensor_event = threading.Event()

  try:
    rpir4_settings = settings['RPIR4']
    rdht4_settings = settings['RDHT4']
    b4sd_settings = settings['B4SD']
    dl_settings = settings['DL']

    # run_dht(rdht4_settings, threads, stop_event)
    
    # run_pir(rpir4_settings, dl_settings, threads, stop_event, rpir4_event)

    run_b4sd(b4sd_settings, threads, stop_event, sensor_event)

    menu(settings)
    raise KeyboardInterrupt

  except KeyboardInterrupt:
    print('Stopping app')
    for t in threads:
      stop_event.set()
