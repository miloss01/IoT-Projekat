
import threading
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.led import run_led
from components.buzz import run_buzz
from components.keypad import run_keypad
import time

# try:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)
# except:
#     pass

def menu(settings):
  print("1 - DS1 - Door Sensor")
  print("2 - DL - Door Light")
  print("3 - DB - Door Buzzer")
  print("4 - DMS - Door Membrane Switch")
  print("X - Exit")

  ds1_settings = settings['DS1']
  dl_settings = settings['DL']
  db_settings = settings['DB']
  dms_settings = settings['DMS']

  while True:
    option = input("")
    if option == "X":
      break
    if option == "1":
      run_button(ds1_settings)
    if option == "2":
      run_led(dl_settings)
    if option == "3":
      run_buzz(db_settings)
    if option == "4":
      run_keypad(dms_settings, "DMS")


if __name__ == "__main__":
  print('Starting app')

  settings = load_settings()
  threads = []
  stop_event = threading.Event()

  dpir1_event = threading.Event()
  rpir1_event = threading.Event()
  rpir2_event = threading.Event()

  try:
    rdht1_settings = settings['RDHT1']
    rdht2_settings = settings['RDHT2']
    dus1_settings = settings['DUS1']
    dpir1_settings = settings['DPIR1']
    rpir1_settings = settings['RPIR1']
    rpir2_settings = settings['RPIR2']

    # run_dht(rdht1_settings, threads, stop_event)
    # run_dht(rdht2_settings, threads, stop_event)
    #
    # run_uds(dus1_settings, threads, stop_event)
    #
    # run_pir(dpir1_settings, threads, stop_event, dpir1_event)
    # run_pir(rpir1_settings, threads, stop_event, rpir1_event)
    # run_pir(rpir2_settings, threads, stop_event, rpir2_event)

    menu(settings)
    raise KeyboardInterrupt

  except KeyboardInterrupt:
    print('Stopping app')
    for t in threads:
      stop_event.set()
