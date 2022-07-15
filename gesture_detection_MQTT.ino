/* Code for gesture input detection and transmission
 * uses mpu6050 imu with ESP12 module 
 * Outputs the x/y acceleration values to Raspberry Pi via MQTT protocol
 */

#include<ESP8266WiFi.h>
#include<Wire.h>
#include <PubSubClient.h>


// ********* INPUTS ****************
const char* ssid = ""; // enter WiFi SSID
const char* password = ""; // enter WiFi Password

const char* mqtt_server = ""; // Raspberry Pi IP address

// *************************************

WiFiClient espClient;
PubSubClient client(espClient);

const uint8_t MPU6050Address = 0x68; //defualt address

const uint8_t scl = D6; // i2c clock pin
const uint8_t sda = D7; // i2c data line pin

const uint16_t AccelScale = 16384;

const uint8_t SMPRT_DIV    =  0x19;
const uint8_t USER_CTRL    =  0x6A;
const uint8_t PWR_MGMT_1   =  0x6B;
const uint8_t PWR_MGMT_2   =  0x6C;
const uint8_t CONFIG       =  0x1A;
const uint8_t GYRO_CONFIG  =  0x1B;
const uint8_t ACCEL_CONFIG =  0x1C;
const uint8_t FIFO_EN      =  0x23;
const uint8_t INT_ENABLE   =  0x38;
const uint8_t ACCEL_XOUT_H =  0x3B;
const uint8_t SIGNAL_PATH_RESET  = 0x68;

int16_t AccelX, AccelY;

void I2C_Write(uint8_t deviceAddress, uint8_t regAddress, uint8_t data){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.write(data);
  Wire.endTransmission();
}

void Read_RawValue(uint8_t deviceAddress, uint8_t regAddress){
  Wire.beginTransmission(deviceAddress);
  Wire.write(regAddress);
  Wire.endTransmission();
  Wire.requestFrom(deviceAddress, (uint8_t)4);
  AccelX = (((int16_t)Wire.read()<<8)|Wire.read()); // acceleration along X axis
  AccelY = (((int16_t)Wire.read()<<8)|Wire.read()); // acceleration along Y axis
 
}

void MPU6050_Init(){
  delay(150);
  I2C_Write(MPU6050Address, SMPRT_DIV, 0x07);
  I2C_Write(MPU6050Address, CONFIG, 0x00);
  I2C_Write(MPU6050Address, GYRO_CONFIG, 0x00);
  I2C_Write(MPU6050Address, ACCEL_CONFIG, 0x00);
  I2C_Write(MPU6050Address, FIFO_EN, 0x00);
  I2C_Write(MPU6050Address, INT_ENABLE, 0x00);
  I2C_Write(MPU6050Address, SIGNAL_PATH_RESET, 0x00);
  I2C_Write(MPU6050Address, USER_CTRL, 0x00);
  I2C_Write(MPU6050Address, PWR_MGMT_1, 0x00);
  I2C_Write(MPU6050Address, PWR_MGMT_2, 0x00);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}


void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
      client.subscribe("esp8266/4");
      client.subscribe("esp8266/5");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(15000);
    }
  }
}


void setup() {

  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
 Wire.begin(sda,scl);
  MPU6050_Init();

  }



void loop() {
if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())

    client.connect("ESP8266Client");
  
  double Ax,Ay;
  Read_RawValue(MPU6050Address, ACCEL_XOUT_H);
  static char accelx[7];
    dtostrf(AccelX, 0, 0, accelx);
    
    static char accely[7];
    dtostrf(AccelY, 0, 0, accely);

   
    // Publishes Temperature and Humidity values
    client.publish("/esp8266/X", accelx);
    client.publish("/esp8266/Y", accely);
    
    Serial.print("X axis: ");
    Serial.print(AccelX);
    Serial.print("\t Y axis: ");
    Serial.print(AccelY);
     Serial.println("");
     
     
delay(40); // (ms) change for lower latency
}
