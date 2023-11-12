
import threading
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
import time

# try:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)
# except:
#     pass


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

    # run_dht(rdht1_settings, threads, stop_event, "RDHT1")
    # run_dht(rdht2_settings, threads, stop_event, "RDHT2")
    # run_uds(dus1_settings, threads, stop_event, "DUS1")

    run_pir(dpir1_settings, threads, stop_event, "DPIR1", dpir1_event)
    run_pir(rpir1_settings, threads, stop_event, "RPIR1", rpir1_event)
    run_pir(rpir2_settings, threads, stop_event, "RPIR2", rpir2_event)

    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print('Stopping app')
    for t in threads:
      stop_event.set()
