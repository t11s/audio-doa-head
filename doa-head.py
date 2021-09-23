#
# info: https://wiki.seeedstudio.com/ReSpeaker-USB-Mic-Array/
#
from tuning import Tuning
import usb.core
import usb.util
import time
import serial

usbPort = '/dev/ttyACM0'
sc = serial.Serial(usbPort, 9600,timeout=1)
 
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
 
if dev:
    Mic_tuning = Tuning(dev)
    while True:
        try:
            if(Mic_tuning.is_voice()):
		doa=Mic_tuning.direction
		print('DOA=',doa)
		if(doa<190):	
			target=int(((((190-doa)/180.0)*1000.0)+1000.0)*4.0)
			print('Moving, target=',target)
			serialBytes = chr(0x84)+chr(0x05)+chr(target & 0x7F)+chr((target >> 7) & 0x7F)
			sc.write(serialBytes)
			time.sleep(1)
		else:
			print('NOT MOVING')
		time.sleep(0.1)
        except KeyboardInterrupt:
            break

sc.close()
