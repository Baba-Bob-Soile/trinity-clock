import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import os.path
from ds18b20 import DS18B20

def plot_temp():
    results_data=np.loadtxt(txt_name,skiprows=1)
    rows=results_data.size/(no_of_sensors+1)
    if rows > 1:
        unix_time=results_data[0:,0]
        date_time= [None] * len(unix_time)
        for index,time_inst in enumerate(unix_time):
            datetime_data=datetime.datetime.fromtimestamp(unix_time[index])
            date_time[index]=datetime_data
            
        plt.figure()
        xfmt = md.DateFormatter('%H:%M')
        xfmtb= md.HourLocator(interval=2)
        legendlabel=[None]*len(np.arange(no_of_sensors))
        for index in np.arange(no_of_sensors):
            legendlabel[index]="Probe {}".format(index+1)
        lineobjects=plt.plot(date_time,results_data[0:,1:])
        plt.title("Temperature vs Time")
        plt.legend(lineobjects,legendlabel)
        plt.ylabel("Temperature (degree Celsius)")
        plt.xlabel("Time in seconds since "+start_time_formatted)
        ax=plt.gca()
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(xfmtb)
        plt.savefig(image_name)
        plt.close()
        return

sensors = DS18B20.get_all_sensors()
no_of_sensors=len(DS18B20.get_available_sensors())
sensor =np.array([])
sensor_header="unixtime  datetime  Probe1(bottom) #2   #3  #4  #5   #6(top)\n"
print(sensor_header)
tic=time.time()
start_time=datetime.datetime.now()
start_time_formatted=start_time.strftime("%Y-%m-%d_%H-%M-%S")
start_time_formatted="test4"
print("In While Loop...")
path="/home/pi/Temperature/"
sensor_data= sensor_header

image_name="{}{}.png".format(path,start_time_formatted)
txt_name="{}{}.txt".format(path,start_time_formatted)

if os.path.isfile(txt_name) != True: 
    f=open("{}".format(txt_name), "a+")
    f.write("{}".format(sensor_header))
f=open("{}".format(txt_name), "a+")
while True:
    tic=time.time()
    unixtime=time.time()
    probe_data=[None]*(no_of_sensors+1)
    probe_data[0]=unixtime

    for index,sensor in enumerate(sensors):
        if index==0: probe_data[6]=round(sensor.get_temperature(),4)
        if index==1: probe_data[4]=round(sensor.get_temperature(),4)
        if index==2: probe_data[3]=round(sensor.get_temperature(),4)
        if index==3: probe_data[5]=round(sensor.get_temperature(),4)
        if index==4: probe_data[1]=round(sensor.get_temperature(),4)
        if index==5: probe_data[2]=round(sensor.get_temperature(),4)
    print probe_data

    f.write("{}  {}  {}  {}  {}  {}  {} \n".format(probe_data[0],probe_data[1],
                                              probe_data[2],probe_data[3],
                                              probe_data[4],probe_data[5],
                                              probe_data[6]))
    f.close
    f=open("{}".format(txt_name), "a+")
    #plot_temp()

    while time.time()-tic<10:
        time.sleep(0.1)
