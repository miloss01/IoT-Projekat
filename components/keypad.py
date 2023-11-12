import time

def run_keypad_simulator(text, code):
  t = time.localtime()
  print(f"Code: {code}, Timestamp: {time.strftime('%H:%M:%S', t)}, {text}")

def run_keypad(settings, code):
  if settings['simulated']:
    run_keypad_simulator(settings["text"], code)