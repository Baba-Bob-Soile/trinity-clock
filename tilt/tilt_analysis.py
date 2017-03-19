from time import sleep
import time
import datetime
import spidev
import matplotlib.pyplot as plt
import matplotlib.dates as md
from scipy import signal
import numpy as np
import os

def noise_filter(input_signal):
        b, a = signal.butter(4, 160, 'low', analog=True)
        output_signal = signal.filtfilt(b, a,input_signal)
        return output_signal
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
def three_moving_average(interval,window_size):
        window = np.ones(int(window_size))/float(window_size)
        first=np.convolve(interval, window, 'same')
        second=np.convolve(first, window, 'same')
        third=np.convolve(second, window, 'same')
        return third
def fifteen_moving_average(interval,window_size):
        third=three_moving_average(interval,window_size)
        sixth=three_moving_average(third,window_size)
        ninth=three_moving_average(sixth,window_size)
        twelfth=three_moving_average(ninth,window_size)
        fifteenth=three_moving_average(twelfth,window_size)
        return fifteenth
def plot_weighted_ma():
        fig, axarr = plt.subplots(4, sharex=True)
        axarr[0].set_title("Tilt Measurements")
        axarr[0].set_ylabel("Inst.")
        axarr[0].plot(time_noise, inst)
        axarr[1].set_ylabel("1st Ave")
        axarr[1].plot(time_noise, first_ave)
        axarr[2].set_ylabel("2nd Ave")
        axarr[2].plot(time_noise, second_ave)
        axarr[3].set_ylabel("Clean")
        axarr[3].plot(time_clean, clean)
        ##axarr[4].set_ylabel("Filtered")
        ##axarr[4].plot(time_noise, filtered)
        fig.savefig("Noise_in_Tilt_Comparison{}_weighted.png".format(filename))
def plot_conv_ma():      
        xfmt = md.DateFormatter('%H:%M')
        xfmtb= md.HourLocator()
        xfmtc= md.MinuteLocator(interval=15)
        fig, axarr = plt.subplots(4, sharex=True)
        time_start=time.strftime("%Y-%m-%d",time.localtime(time_noise[1]))
        axarr[0].set_title("Tilt Measurements from {}".format(time_start))
        axarr[0].set_ylabel("Inst.")
        axarr[0].plot(datetime_noise, inst)
        axarr[1].set_ylabel("3 MA")
        axarr[1].plot(datetime_noise, mov_ave)
        axarr[2].set_ylabel("18 MA")
        axarr[2].plot(datetime_noise, mov_ave_second)
        axarr[3].set_ylabel("33 MA")
        axarr[3].plot(datetime_noise, mov_ave_three)
        
        ax=plt.gca()
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(xfmtb)
        #ax.xaxis.set_minor_locator(xfmtc)
        
        fig.savefig("Noise_in_Tilt_Comparison_{}_conv.png".format(name))

print "Enter a file name:",
name = raw_input()
tic=time.time()
path="/home/pi/"
#name="tilt8b"
#name="2017-02-22_16-41-00"
prefix="tilt_{}".format(name)
suffix="_after.txt"
dirs = os.listdir( path )
filenamelist=[]
for f in dirs:
        if f.startswith(prefix) and f.endswith(suffix):
                filenamelist.extend([f])
filenamelist.sort()

for index, filename in enumerate(filenamelist):
        print index, filename
        new_data=np.loadtxt(filename,skiprows=1)
        if index==0:
                tilt_noise=new_data
        else:
                tilt_noise=np.vstack((tilt_noise, new_data))

time_noise=tilt_noise[0:,0]
datetime_noise= [None] * len(tilt_noise)
for index,time_noise_inst in enumerate(time_noise):
        unix_time_f=time_noise[index]
        datetime_data=datetime.datetime.fromtimestamp(unix_time_f)
        datetime_noise[index]=datetime_data
inst=tilt_noise[0:,1]
#To select certain regions
##start=1000
##end=start+3600*16
##datetime_noise=datetime_noise[start:end]
##inst=inst[start:end]

window=10*16
mov_ave=three_moving_average(inst,window)
mov_ave_second=fifteen_moving_average(mov_ave,window)
mov_ave_three=fifteen_moving_average(mov_ave_second,window)
plot_conv_ma()

smooth_results=np.column_stack((time_noise, datetime_noise, inst, mov_ave, mov_ave_second, mov_ave_three))
np.savetxt("{}_smooth.txt".format(prefix),smooth_results,
                             delimiter="  ", fmt="%s",
                             header="unixtime  datetime  inst.  Filter1  Filter2   Filter 3  ")
toc=time.time()
print "Runtime:{}".format(toc-tic)

                  


        
