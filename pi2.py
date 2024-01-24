
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
from components.gyro import run_gyro
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

  dpir2_event = threading.Event()
  rpir3_event = threading.Event()
  sensor_event = threading.Event()
  gsg_event = threading.Event()

  try:
    gdht_settings = settings['GDHT']
    ds2_settings = settings['DS2']
    dus2_settings = settings['DUS2']
    dpir2_settings = settings['DPIR2']
    rpir3_settings = settings['RPIR3']
    rdht3_settings = settings['RDHT3']
    gsg_settings = settings['GSG']
    dl_settings = settings['DL']

    # run_dht(gdht_settings, threads, stop_event)
    # run_dht(rdht3_settings, threads, stop_event)
    
    # run_uds(dus2_settings, threads, stop_event)
    
    # run_pir(dpir2_settings, dl_settings, threads, stop_event, dpir2_event)
    # run_pir(rpir3_settings, dl_settings, threads, stop_event, rpir3_event)

    # run_button(ds2_settings, threads, stop_event, sensor_event)
    # run_gyro(gsg_settings, threads, stop_event, gsg_event)

    menu(settings)
    raise KeyboardInterrupt

  except KeyboardInterrupt:
    print('Stopping app')
    for t in threads:
      stop_event.set()
