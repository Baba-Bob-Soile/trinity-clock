from __future__ import print_function
from time import sleep
from scipy import signal
import numpy as np
import time
import datetime
import spidev
import matplotlib.pyplot as plt
 
# Open SPI bus
spi = spidev.SpiDev()
spi.close()
spi.open(0,0)
spi.max_speed_hz = 10000#150000
spi.cshigh = False

def twos_complement(input_value, num_bits):
	#Calculates a two's complement integer
        #from the given input value's bits
	mask = 2**(num_bits - 1)
	return -(input_value & mask) + (input_value & ~mask)
def ConvertVolts(data,places):
  offset= 0 #0.007
  volts = (data * 4.096) / float(pow(2,16))
  volts = round(volts,places)+offset
  return volts

def noise_filter(input_signal):
        b, a = signal.butter(4, 0.67, 'low', analog=True)
        output_signal = signal.filtfilt(b, a,input_signal)
        
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

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
        axarr[3].plot(time_noise, mov_ave_third)        
        fig.savefig("Noise_in_Tilt_Comparison_{}_conv.png".format(time_formatted))
        plt.close(fig)

#Function to read SPI data from LTC1867 chip
# Channel must be an integer 0-7
def ReadChannel():
  #Performs an SPI transaction.
  #Chip-select should be held active between blocks.
  #pi.spi_xfer([XXXXXXX,0])#sends 2 bytes 1st contains DIN, second is irrelevant
  #See http://cds.linear.com/docs/en/datasheet/18637fc.pdf for more info
  #pin 7-GND=[244,0] connected to ground
  #pin 6-GND=[180,0]
  #pin 5-GND=[228,0] connected to 2.5V
  #pin 1-GND=[196,0]
  #pin 1-pin 2= [0,0]connected to analog level
  #pin 6-pin 7= [48,0] should be 2.5V

  channel_six = spi.xfer2([180,0])
  channel_seven = spi.xfer2([244,0])
  tilt = spi.xfer2([0,0])
  
  six_data = (channel_six[0]<<8) + channel_six[1]
  sev_data = (channel_seven[0]<<8) + channel_seven[1]

  tilt_data = (tilt[0]<<8) + tilt[1]
  dummy=six_data
  six_data=sev_data
  sev_data=tilt_data
  tilt_data=dummy
  tilt_data = twos_complement(tilt_data,16)
  tilt_measured=ConvertVolts(tilt_data,4)
  tilt_corrected=tilt_measured*float(40000/six_data)
  return tilt_corrected

print("Reading LTC1867 values, press Ctrl-C to quit...")

delay=0.05
reading=ReadChannel()
index=0
saved=False
written=0
header="time  inst.\n"

tic= time.time()
datetime_now=datetime.datetime.now()
time_formatted=datetime_now.strftime("%Y-%m-%d_%H-%M-%S")
##time_formatted="49_60_batt"
filename="tilt_{}".format(time_formatted)
filename_txt= "{}_1_hr_after.txt".format(filename,0)
f=open("{}".format(filename_txt), "a+")
f.write("{}".format(header))
while True:
          time_now=time.time()
          tilt_inst = ReadChannel()
          index=index +1
          sleep(delay)
          
          f.write("{}  {}\n".format(time_now, tilt_inst))
          
          timediff=time_now-tic
          timediff_secs=int(timediff)
          no_hours= timediff_secs/3600
          if timediff_secs%5==0 and timediff_secs>4:
                  print(index, timediff, no_hours, tilt_inst)
                  f.close
                  f=open("{}".format(filename_txt), "a+")
          if timediff_secs%3600==0 and no_hours>0 and written != no_hours:
                  print("Saving new hour data to new file")
                  results=[time_now,tilt_inst]
                  written=no_hours
                  if no_hours==24:
                          break
                  filename_txt="{}_{}_hr_after.txt".format(filename,no_hours+1)
                  f=open("{}".format(filename_txt), "a+")
                  f.write("{}".format(header))
                      
          if saved:
##                  tictic=datetime.datetime.now()
##                  tilt_noise=np.loadtxt("{}".
##                                        format(filename_txt),skiprows=2)
##                  time_noise=tilt_noise[0:,0]
##                  inst=tilt_noise[0:,1]
##                  mov_ave=movingaverage(inst,10)
##                  mov_ave_second=movingaverage(mov_ave,10)
##                  mov_ave_third=movingaverage(mov_ave_second,10)
##                  plot_conv_ma()
##                  toctoc=datetime.datetime.now()
##                  time_taken=toctoc-tictic
##                  time_secs=time_taken.total_seconds()
##                  print "time taken{}".format(time_secs)
##                  smoothresults=np.hstack((results, [mov_ave,
##                                                     mov_ave_second,
##                                                     mov_ave_third]))
##                  np.savetxt("{}_smooth.txt".format(filename),results,
##                             delimiter="  ", fmt="%s",
##                             header="time  inst.  1st MA    2nd MA    3rd MA")
                  saved=False
          

                  
                  


        
