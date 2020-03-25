# -*- coding: utf-8 -*
import serial
import time
import RPi.GPIO as GPIO #i need those libraries to control my pins!
import numpy as np
import matplotlib.pyplot as plt #i need it to plot!
import matplotlib.animation as animation
ser = serial.Serial('/dev/ttyAMA0', 115200)
PwmPin1 = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Sposób numerowania Pinów
GPIO.setup(PwmPin1,GPIO.OUT) #Definicja Pinu
pi_pwm = GPIO.PWM(PwmPin1,1000) #GPIO.PWM(channel, frequency)
pi_pwm.start(80) #%Wypełnienia sygnału w trakcie jednego okresu.
GPIO.setup(PwmPin1, GPIO.OUT)


def getTFminiData(): #Definicja Funkcji.
    millis1 = int(round(time.time() * 1000)) #klasyk, zbierz czas do roznicy
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
                #print(millis-millis1), #przecinek pozwala na printline.
                #print(distance)
                return distance
                
def plotMydata(r):
    #r = np.arange(0, 2, 0.01)
    #theta = 2 * np.pi * r
    ax = plt.subplot(111, projection='polar') #polar coordinates.
    ax.scatter(np.pi, r) 
    ax.set_rmax(300) #setmax.
    ax.set_rticks([0.5, 1, 1.5, 2, 2.5, 3 ,3.5, 4, 4.5, 10])  # Less radial ticks, i really want to do it procedurally.
    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)
    ax.set_title("A line plot on a polar axis", va='bottom')
    plt.show() #Yeah, its showing data but one measure point!, i need to animate it.
                      
if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        x = getTFminiData()
        plotMydata(x)
        
        
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
