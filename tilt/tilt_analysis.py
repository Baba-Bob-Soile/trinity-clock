from time import sleep
import time
import datetime
import spidev
import matplotlib.pyplot as plt
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
        fig, axarr = plt.subplots(4, sharex=True)
        axarr[0].set_title("Tilt Measurements")
        axarr[0].set_ylabel("Inst.")
        axarr[0].plot(datetime_noise, inst)
        axarr[1].set_ylabel("6 MA")
        axarr[1].plot(datetime_noise, mov_ave)
        axarr[2].set_ylabel("12 MA")
        axarr[2].plot(datetime_noise, mov_ave_second)
        axarr[3].set_ylabel("27 MA")
        axarr[3].plot(datetime_noise, mov_ave_three)
        fig.savefig("Noise_in_Tilt_Comparison_{}_conv.png".format(name))


path="/home/pi/"
#name="tilt9_1_hr_after"
name="2017-02-22_20-53-28"
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
datetime_noise=np.empty(np.size(time_noise),dtype="datetime64[ms]")
for index,time_noise_inst in enumerate(time_noise):
        unix_time_f=time_noise[index]
        datetime_data=datetime.datetime.fromtimestamp(unix_time_f).strftime('%Y-%m-%d %H:%M:%S.%f')
        datetime_noise[index]=str(datetime_data)
inst=tilt_noise[0:,1]
#To select certain regions
##start=1000
##end=start+3600*16
##time_noise=tilt_noise[start:end,0]
##inst=tilt_noise[start:end,1]
window=3*16
mov_ave=three_moving_average(three_moving_average(inst,window),window*3)
mov_ave_second=three_moving_average(three_moving_average(mov_ave,window),window)
mov_ave_three=fifteen_moving_average(mov_ave_second,window*3)


plot_conv_ma()

                  
