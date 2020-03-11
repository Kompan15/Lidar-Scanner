#include <SoftwareSerial.h>  //header file of software serial port 
#include <Servo.h> 
SoftwareSerial Serial1(2, 3); //define software serial port name as Serial1 and define pin2 as RX and pin3 as TX
int Step=10;
int Dir =11;
int Ena =9;
int stepTime=1000;
float angle = 0;
bool dirL = 1;
int dist; //actual distance measurements of LiDAR
int strength; //signal strength of LiDAR
float temprature;
int check;  //save check value
int p;
int i;
int uart[9];  //save data measured by LiDAR
const int HEADER = 0x59; //frame header of data package
Servo Servo1;
void setup() {
  pinMode(Step, OUTPUT);
  pinMode(Dir, OUTPUT);
  pinMode(Ena, OUTPUT);
  Serial.begin(115200); //set bit rate of serial port connecting Arduino with computer
  Serial1.begin(115200);  //set bit rate of serial port connecting LiDAR with Arduino
}
void loop() {
    if (Serial1.available()) {  //check if serial port has data input
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
          digitalWrite(Ena, HIGH);
          if (angle >= 360){ dirL = !dirL; angle = 0; Serial.println("KONIEC SERII!!!");}
          digitalWrite(Dir, dirL);
          digitalWrite(Step, HIGH);   
          delayMicroseconds(stepTime);                      
          digitalWrite(Step, LOW);    
          delayMicroseconds(stepTime);
          angle+=0.45;
         
          Serial.print(dist); //output measure distance value of LiDAR
         
          Serial.print(":");
          Serial.println(angle); //output chip temperature of Lidar
        }
      }
    }
  }
   }