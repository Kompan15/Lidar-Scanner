# -*- coding: utf-8 -*
import serial
import time
import RPi.GPIO as GPIO #i need those libraries to control my pins!
import numpy as np
import matplotlib.pyplot as plt #i need it to plot!
import matplotlib.animation as animation
from time import sleep
ser = serial.Serial('/dev/ttyAMA0', 115200)
PwmPin1 = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Sposób numerowania Pinów
GPIO.setup(PwmPin1,GPIO.OUT) #Definicja Pinu
pi_pwm = GPIO.PWM(PwmPin1,3000) #GPIO.PWM(channel, frequency)
pi_pwm.start(20) #%Wypełnienia sygnału w trakcie jednego okresu.
GPIO.setup(PwmPin1, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
#global objects
fig = plt.figure()
ax = plt.subplot(111, polar=True)
theta = []
dis = []
angle = 0
def pulse():
    GPIO.output(24, 1)
    GPIO.output(24, 0)
    global angle
    angle += 0.08
    return angle
 
def getTFminiData(): #Definicja Funkcji.
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y': # 0x59s to 'Y', To są pierwsze dwa bajty info.
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                distance = low + high * 256
                millis = int(round(time.time() * 1000)) #Zbierz czas na zakonczenie funkcji.
                return distance
                
def animate(i, theta, dis):
    theta.append(pulse())
    dis.append(getTFminiData())
    #Limits
    theta = theta[-50:]
    dis = dis[-50:]
    #Draw
    ax.clear()
    ax.scatter(theta, dis)
    # Format plot
    plt.title('radial')
                
ax.set_rmax(100)			#Not really neccesary
ax.set_rticks([0.5, 1, 1.5, 2, 2.5, 3 ,3.5, 4, 4.5, 10])      #Not really neccesary
ani = animation.FuncAnimation(fig, animate, fargs=(theta, dis), interval=110)              
plt.show()      
           
if __name__ == '__main__': 
    try:
        if ser.is_open == False:
            ser.open()
        
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()