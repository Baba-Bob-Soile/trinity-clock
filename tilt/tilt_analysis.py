from time import sleep
import time
import datetime
import spidev
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

def noise_filter(input_signal):
        b, a = signal.butter(4, 0.067, 'low', analog=True)
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
        axarr[0].plot(time_noise, inst)
        axarr[1].set_ylabel("1 MA")
        axarr[1].plot(time_noise, mov_ave)
        axarr[2].set_ylabel("2 MA")
        axarr[2].plot(time_noise, mov_ave_second)
        axarr[3].set_ylabel("3 MA")
        axarr[3].plot(time_noise, mov_ave_three)        
        fig.savefig("Noise_in_Tilt_Comparison{}_conv.png".format(filename))

filename="_tilt9_1_hr_after"
#filename="_2017-02-22_20-53-28"#_3_hr_after"#33-58,16-31-10
#tilt_noise=np.loadtxt("tilt_data{}.txt".format(filename),skiprows=2)
tilt_noise=np.loadtxt("tilt{}.txt".format(filename),skiprows=2)
#tilt_clean=np.loadtxt("tilt_smooth{}.txt".format(filename),skiprows=2)


time_noise=tilt_noise[0:,0]
#time_clean=tilt_clean[0:,0]
inst=tilt_noise[0:,1]
#first_ave=tilt_noise[0:,2]
#second_ave=tilt_noise[0:,3]
#clean=tilt_clean[0:,1]
filtered= noise_filter(inst)
mov_ave=movingaverage(inst,10)
mov_ave_second=movingaverage(mov_ave,10)
mov_ave_three=movingaverage(mov_ave_second,10)


#plot_weighted_ma()
plot_conv_ma()

                  

