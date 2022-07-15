import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
AccelScale = 16384   # accelerometer scale

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27,GPIO.OUT)  # IN1
    GPIO.setup(22,GPIO.OUT)  # N2
    GPIO.setup(23,GPIO.OUT)  # IN3
    GPIO.setup(24,GPIO.OUT)  # IN4
    GPIO.setup(4,GPIO.OUT)   # ENA
    GPIO.setup(26,GPIO.OUT)  # ENB
    pwm1 = GPIO.PWM(4, 100)
    pwm2 = GPIO.PWM(26, 100)
    pwm1.start(100) # Left motor pwm frequency
    pwm2.start(100) # Right motor pwm frequency
    
def reverse(tf):
    init()
    GPIO.output(27,GPIO.LOW)
    GPIO.output(22,GPIO.HIGH)
    GPIO.output(23,GPIO.HIGH)
    GPIO.output(24,GPIO.LOW)
    pwm1.ChangeDutyCycle(40)
    pwm2.ChangeDutyCycle(40)
    time.sleep(tf)
    GPIO.cleanup()
    
def forward(tf):
    init()
    GPIO.output(27,GPIO.HIGH)
    GPIO.output(22,GPIO.LOW)
    GPIO.output(23,GPIO.LOW)
    GPIO.output(24,GPIO.HIGH)
    pwm1.ChangeDutyCycle(40)
    pwm2.ChangeDutyCycle(40)
    time.sleep(tf)
    GPIO.cleanup()
    
def left(tf):
    init()
    GPIO.output(27,GPIO.LOW)
    GPIO.output(22,GPIO.HIGH)
    GPIO.output(23,GPIO.LOW)
    GPIO.output(24,GPIO.HIGH)
    pwm1.ChangeDutyCycle(80)
    pwm2.ChangeDutyCycle(80)
    time.sleep(tf)
    GPIO.cleanup()
    
def right(tf):
    init()
    GPIO.output(27,GPIO.HIGH)
    GPIO.output(22,GPIO.LOW)
    GPIO.output(23,GPIO.HIGH)
    GPIO.output(24,GPIO.LOW)
    pwm1.ChangeDutyCycle(80)
    pwm2.ChangeDutyCycle(80)
    time.sleep(tf)
    GPIO.cleanup()

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
            left(0.01)
            
        if (Ax < -0.5):
            right(0.01)
        
    if (message.topic == "/esp8266/Y"):
        yint = float(message.payload)
        
        Ay = (yint/(AccelScale))
        print("AccY: ",Ay)
        if (Ay < -0.5):
            
            forward(0.015)
        
            
        if (Ay > 0.5):
            reverse(0.015)
        
            
        
        print(".....................")
            
        
def main():
    
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('localhost', 1883, 60) 
    # Connect to the MQTT server and process messages in a background thread. 
    mqtt_client.loop_start()
    
    
main()





