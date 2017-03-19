import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
from ds18b20 import DS18B20

sensors = DS18B20.get_all_sensors()
no_of_sensors=len(DS18B20.get_available_sensors())
print("Number of sensors", no_of_sensors)
sensor =np.array([])
#sensor_header=np.append(["Time","Time Perf"],DS18B20.get_available_sensors())
sensor_header="unixtime  datetime  Probe1(bottom) #2   #3  #4  #5   #6(top)\n"
print(sensor_header)
tic=time.time()
start_time=datetime.datetime.now()
start_time_formatted=start_time.strftime("%Y-%m-%d_%H-%M-%S")
start_time_formatted="test"
print("In While Loop...")
path="/home/pi/Temperature/"
sensor_data= sensor_header

image_name="{}{}.png".format(path,start_time_formatted)
txt_name="{}{}.txt".format(path,start_time_formatted)

f=open("{}".format(txt_name), "a+")
f.write("{}".format(sensor_header))
while True: 
    data=np.array([])
    unixtime=time.time()
    #date_time=datetime.datetime.fromtimestamp(unixtime)
    #data=np.append(data,[unixtime,date_time])
    data=np.append(data,[unixtime])
    
    for sensor in sensors:
        data=np.append(data, sensor.get_temperature())

    probe_data= [None] * len(data)
    probe_data[0]=data[0]
    probe_data[1]=data[1]
    probe_data[2]=round(data[6],4)
    probe_data[3]=round(data[7],4)
    probe_data[4]=round(data[4],4)
    probe_data[5]=round(data[3],4)
    probe_data[6]=round(data[5],4)
    probe_data[7]=round(data[2],4)
    print data[2:]
    print probe_data[2:]
    print "*******************************************"

    f.write("{}  {}  {}  {}  {}  {}  {}  {}\n".format(probe_data[0],probe_data[1],
                                              probe_data[2],probe_data[3],
                                              probe_data[4],probe_data[5],
                                              probe_data[6],probe_data[7]))
    f.close
    f=open("{}".format(txt_name), "a+")
    results_data=np.loadtxt(txt_name,skiprows=1,dtype="str")

    datetime=results_data[0:,1]
    plt.figure()
    plt.scatter(datetime,results_data[0:,2:])
    plt.title("Temperature vs Time")
    plt.ylabel("Temperature (degree Celsius")
    plt.xlabel("Time in seconds since "+start_time_formatted)
    plt.savefig(image_name)

    time.sleep(1)



