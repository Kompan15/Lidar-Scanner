#include <SoftwareSerial.h>  //header file of software serial port 
#include <Servo.h> 
SoftwareSerial Serial1(2, 3); //define software serial port name as Serial1 and define pin2 as RX and pin3 as TX
int dist; //actual distance measurements of LiDAR
int strength; //signal strength of LiDAR
float temprature;
int check;  //save check value
int p;
int i;
int uart[9];  //save data measured by LiDAR
const int HEADER = 0x59; //frame header of data package
int servoPin = 5;
Servo Servo1;
void setup() {
  Servo1.attach(servoPin);
  Serial.begin(115200); //set bit rate of serial port connecting Arduino with computer
  Serial1.begin(115200);  //set bit rate of serial port connecting LiDAR with Arduino
}
void loop() {
  for(int p = 0; p<=180; p++){
    Servo1.write(p);
    delay(20);
    while (Serial1.available()) {  //check if serial port has data input
    if (Serial1.read() == HEADER) { //assess data package frame header 0x59
      uart[0] = HEADER;
      if (Serial1.read() == HEADER) { //assess data package frame header 0x59
        uart[1] = HEADER;
        for (i = 2; i < 9; i++) { //save data in array
          uart[i] = Serial1.read();
        }
        check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];
        if (uart[8] == (check & 0xff)) { //verify the received data as per protocol
          dist = uart[2] + uart[3] * 256;     //calculate distance value
          strength = uart[4] + uart[5] * 256; //calculate signal strength value
          temprature = uart[6] + uart[7] * 256; //calculate chip temprature
          temprature = temprature / 8 - 256;
          //Serial.print("dist = ");
          Serial.print(dist); //output measure distance value of LiDAR
          //Serial.print('\t');
         // Serial.print("strength = ");
         // Serial.print(strength); //output signal strength value
          //Serial.print("\t Chip Temprature = ");
          //Serial.print(temprature);
        //  Serial.println(" celcius degree"); //output chip temperature of Lidar
        Serial.print(":");
          Serial.println(p); //output chip temperature of Lidar
        }
      }
    }
  }
   // Make servo go to 0 degrees 
    
  }
Serial.println(" /////////////////////////////////////////////////// "); //output chip temperature of Lidar
  
  for(int p = 180; p>=0; p--){
    Servo1.write(p);
    delay(20);
    while (Serial1.available()) {  //check if serial port has data input
    if (Serial1.read() == HEADER) { //assess data package frame header 0x59
      uart[0] = HEADER;
      if (Serial1.read() == HEADER) { //assess data package frame header 0x59
        uart[1] = HEADER;
        for (i = 2; i < 9; i++) { //save data in array
          uart[i] = Serial1.read();
        }
        check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];
        if (uart[8] == (check & 0xff)) { //verify the received data as per protocol
          dist = uart[2] + uart[3] * 256;     //calculate distance value
          strength = uart[4] + uart[5] * 256; //calculate signal strength value
          temprature = uart[6] + uart[7] * 256; //calculate chip temprature
          temprature = temprature / 8 - 256;
         //Serial.print("dist = ");
          Serial.print(dist); //output measure distance value of LiDAR
        // Serial.print('\t');
         // Serial.print("strength = ");
         // Serial.print(strength); //output signal strength value
          //Serial.print("\t Chip Temprature = ");
          //Serial.print(temprature);
           Serial.print(":");
        //  Serial.println(" celcius degree"); //output chip temperature of Lidar
          Serial.println(p); //output chip temperature of Lidar
        }
      }
    }
  }
   // Make servo go to 0 degrees 
  }
  
}