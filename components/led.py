import time

working = False

def run_led_simulator(code):
  t = time.localtime()

  global working
  working = not working

  if working:
    on = "on"
  else:
    on = "off"

  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Door light (LED) is turned {on}")

def run_led(settings, code):
  if settings['simulated']:
    run_led_simulator(code)