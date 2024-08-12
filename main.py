import time
from tcs3200 import TCS3200

sensor = TCS3200()
sensor.calibrate()
    
while True:
  sensor.i = 0
  rgb = sensor.get_rgb()
  print(rgb) # Or rgb[0], ...
  time.sleep(4)
