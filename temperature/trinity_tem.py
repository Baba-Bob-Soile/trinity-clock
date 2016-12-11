import os
import time
import glob

#Setup Device on system? 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#Go to device? 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#Function to read temperature
def read_temp():
    f = open(device_file, 'r') #Open Device
    lines = f.readlines()      #Read temp from device line   
    f.close()
    equals_pos = lines[1].find('t=')#Find Part of string in device lines where temp reading is
    if equals_pos != -1:
        tempstring = lines[1][equals_pos+2:]
        temp_c = float(tempstring) / 1000.0
    return temp_c

while True:
    print(read_temp())	
    time.sleep(30)
