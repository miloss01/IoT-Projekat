import time
# import RPi.GPIO as GPIO

def run_button_simulator(code):
  t = time.localtime()
  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Button clicked.")

# def button_pressed():
#   t = time.localtime()
#   print(f"Timestamp: {time.strftime('%H:%M:%S', t)}, Button clicked.")

# def run_button_real(settings, code):
#   port_button = settings["port_button"]
#   GPIO.setmode(GPIO.BCM)
#   GPIO.setup(port_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#   GPIO.add_event_detect(port_button, GPIO.RISING, callback = button_pressed, bouncetime = 100)

def run_button(settings, code):
  if settings['simulated']:
    run_button_simulator(code)
  # else:
  #   run_button_real(settings, code)
