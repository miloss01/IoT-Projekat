import time

def run_buzz_simulator(code):
  t = time.localtime()
  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, Buzzzzz")

def run_buzz(settings, code):
  if settings['simulated']:
    run_buzz_simulator(code)