import paho.mqtt.client as mqtt
import time
import RPi.GPIO as gpio
AccelScale = 16384
appendLeft = '\nleft(0.01)'
appendRight = '\nright(0.01)'
appendForward = '\nforward(0.025)'
appendReverse = '\nreverse(0.025)'
appendStop = '\nstop(0.025)'

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
    


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    client.subscribe("/esp8266/X")
    client.subscribe("/esp8266/Y")

def on_message(client, userdata, message):
    
    if (message.topic == "/esp8266/X"):
        xint = float(message.payload)
        
        Ax = (xint/(AccelScale))
        print("AccX: ",Ax)
        if (Ax > 0.5):
            left(0.007)
            appendFile = open("path.txt","a")
            appendFile.write(appendLeft)
            appendFile.close()
        else:
            
            appendFile = open("path.txt","a")
            appendFile.write(appendStop)
            appendFile.close()
            
        if (Ax < -0.5):
            right(0.007)
            appendFile = open("path.txt","a")
            appendFile.write(appendRight)
            appendFile.close()
        else:
            
            appendFile = open("path.txt","a")
            appendFile.write(appendStop)
            appendFile.close()
        
    if (message.topic == "/esp8266/Y"):
        yint = float(message.payload)
        
        Ay = (yint/(AccelScale))
        print("AccY: ",Ay)
        if (Ay < -0.5):
            
            forward(0.015)
            appendFile = open("path.txt","a")
            appendFile.write(appendForward)
            appendFile.close()
        else:
            
            appendFile = open("path.txt","a")
            appendFile.write(appendStop)
            appendFile.close()
            
        if (Ay > 0.5):
            reverse(0.015)
            appendFile = open("path.txt","a")
            appendFile.write(appendReverse)
            appendFile.close()
        else:
            
            appendFile = open("path.txt","a")
            appendFile.write(appendStop)
            appendFile.close()
            
        
        print(".....................")
            
        
def main():
    
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('localhost', 1883, 60) 
    # Connect to the MQTT server and process messages in a background thread. 
    mqtt_client.loop_start()
    
    
main()