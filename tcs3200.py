import time
import _thread
from machine import Pin

class TCS3200:
    def __init__(self):
        self.g_count = 0
        self.g_array = [0, 0, 0]
        self.g_SF = [0, 0, 0]
        self.i = 0
        
        # Define pins and their initialization
        self.S0 = Pin(18, Pin.OUT)
        self.S1 = Pin(19, Pin.OUT)
        self.S2 = Pin(20, Pin.OUT)
        self.S3 = Pin(21, Pin.OUT)
        self.LED = Pin(16, Pin.OUT)
        
        # GPIO_OUT FREQUENCY SCALING 2%
        self.S0(1)
        self.S1(0)
        self.LED(1)
        
        self.button_red = Pin(17, Pin.IN, Pin.PULL_DOWN)
        self.button_red.irq(trigger=Pin.IRQ_FALLING, handler=self.int_handler)
        
        # Start the second core for color sensing
        _thread.start_new_thread(self.TSC_Callback, ())

    def int_handler(self, pin):
        self.button_red.irq(handler=None)  # OFF IRQ
        self.g_count += 1
        self.button_red.irq(handler=self.int_handler)  # ON IRQ

    def TSC_Callback(self):
        while True:
            time.sleep(1)
            if self.i == 0:
                self.i += 1
                self.g_count = 0
                # Filter: Red
                self.S2(0)
                self.S3(0)
            elif self.i == 1:
                self.g_array[0] = self.g_count
                self.g_count = 0
                self.i += 1
                # Filter: Green
                self.S2(1)
                self.S3(1)
            elif self.i == 2:
                self.g_array[1] = self.g_count
                self.g_count = 0
                self.i += 1
                # Filter: Blue
                self.S2(0)
                self.S3(1)
            elif self.i == 3:
                self.g_array[2] = self.g_count
                self.g_count = 0
                self.i += 1
                # No filter
                self.S2(1)
                self.S3(0)
            else:
                self.g_count = 0

    def calibrate(self):
        print("Calibrating TCS3200 ...")
        time.sleep(5)
        self.g_SF[0] = 255.0 / self.g_array[0]   # R Scale factor
        self.g_SF[1] = 255.0 / self.g_array[1]   # G Scale factor
        self.g_SF[2] = 255.0 / self.g_array[2]   # B Scale factor
        print("Done.")

    def get_rgb(self):
        rgb_values = []
        for j in range(3):
            val = int(self.g_array[j] * self.g_SF[j])
            if val > 255:
                val = 255
            rgb_values.append(val)
        return rgb_values
