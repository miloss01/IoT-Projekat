import time

def run_button_simulator(code):
  t = time.localtime()
  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Button clicked.")

def run_button(settings, code):
  if settings['simulated']:
    run_button_simulator(code)