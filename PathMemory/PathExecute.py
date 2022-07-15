import time
import RPi.GPIO as gpio

with open('path.txt') as f:
    path = []
    for line in f:
        path.append(line.strip("\n"))

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(27,gpio.OUT)
    gpio.setup(22,gpio.OUT)
    gpio.setup(23,gpio.OUT)
    gpio.setup(24,gpio.OUT)
    
def reverse(tf):
    init()
    gpio.output(27,False)
    gpio.output(22,True)
    gpio.output(23,True)
    gpio.output(24,False)
    time.sleep(tf)
    gpio.cleanup()
    
def forward(tf):
    init()
    gpio.output(27,True)
    gpio.output(22,False)
    gpio.output(23,False)
    gpio.output(24,True)
    time.sleep(tf)
    gpio.cleanup()
    
def right(tf):
    init()
    gpio.output(27,True)
    gpio.output(22,False)
    gpio.output(23,True)
    gpio.output(24,False)
    time.sleep(tf)
    gpio.cleanup()

def left(tf):
    init()
    gpio.output(27,False)
    gpio.output(22,True)
    gpio.output(23,False)
    gpio.output(24,True)
    time.sleep(tf)
    gpio.cleanup()

def stop(tf):
    init()
    gpio.output(27,False)
    gpio.output(22,False)
    gpio.output(23,False)
    gpio.output(24,False)
    time.sleep(tf)
    gpio.cleanup()


    
def main():
    
    for element in path:
        if (element == "forward(0.025)"):
            forward(0.015)
            
        if (element == "reverse(0.025)"):
            reverse(0.015)
            
        if (element == "left(0.01)"):
            left(0.007)
            
        if (element == "right(0.01)"):
            right(0.007)
            
        if (element == "stop(0.025)"):
            stop(0.01)
            

main()
        
