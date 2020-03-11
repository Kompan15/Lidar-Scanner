# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)

def getTFminiData():
    millis1 = int(round(time.time() * 1000)) #klasyk, zbierz czas do roznicy
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y': # 0x59s to 'Y', bez interpretacji terminal wypluwa same YYYY
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                distance = low + high * 256
                millis = int(round(time.time() * 1000))
                print(millis-millis1), #przecinek pozwala na printline.
                print(distance)
                
                
if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        getTFminiData()
        
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
