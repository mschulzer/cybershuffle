from machine import Pin,Timer
import time
import _thread

# TCS3200
# https://www.waveshare.com/wiki/Color_Sensor#Specifications


g_count = 0              # count the frequecy
adj_num = 0              # store the RGB value
g_array = [0, 0, 0]      # filter of RGB queue
g_SF    = [0, 0, 0]      # save the RGB Scale factor

# Define pins and their initialization
S0  = machine.Pin(18, machine.Pin.OUT)
S1  = machine.Pin(19, machine.Pin.OUT)
S2  = machine.Pin(20, machine.Pin.OUT)
S3  = machine.Pin(21, machine.Pin.OUT)
LED = machine.Pin(16, machine.Pin.OUT)

# GPIO_OUT FREQUENCY SCALING 2%
S0(1)
S1(0)
LED(1)


button_red = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)

def int_handler(pin):
    button_red.irq(handler=None) #OFF IRQ

    global g_count
    g_count = g_count + 1
    button_red.irq(handler=int_handler) #ON IRQ

button_red.irq(trigger=machine.Pin.IRQ_FALLING, handler=int_handler)


i=0
def TSC_Callback():
    global i
    global g_array
    global g_count
    while True:
        time.sleep(1)
        if(i == 0):
            print("->WB Start")
            i = i + 1
            g_count = 0
            # Filter: Red
            S2(0)
            S3(0)
        elif i == 1:
            print("->Frequency R=", g_count)
            g_array[0] = g_count
            g_count = 0
            i = i + 1
            # Filter: Green
            S2(1)
            S3(1)
        elif i == 2:
            print("->Frequency G=", g_count)
            g_array[1] = g_count
            g_count = 0
            i = i + 1
            # Filter: Blue
            S2(0)
            S3(1)
        elif i == 3:
            print("->Frequency B=", g_count)
            g_array[2] = g_count
            g_count = 0
            i = i + 1
            print("->WB Endr")
            # No filter
            S2(1)
            S3(0)
        else:
            g_count = 0

#Turn on the second core
_thread.start_new_thread(TSC_Callback, ())

if __name__ == "__main__":

    time.sleep(5)
    for j in range(3):
        print(g_array[j])
    g_SF[0] = 255.0 / g_array[0]   #R Scale factor
    g_SF[1] = 255.0 / g_array[1]   #G Scale factor
    g_SF[2] = 255.0 / g_array[2]   #B Scale factor
    for j in range(3):
        print(g_SF[j])
    
    while True:
        i = 0

        for j in range(3):
            if((int)(g_array[j] * g_SF[j]) > 255) :
                print("255")
            else :
                print((int)(g_array[j] * g_SF[j]))
        time.sleep(4)


        
        
