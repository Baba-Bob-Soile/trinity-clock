#Python 3.2.3 (default, Mar  1 2013, 11:53:50) 
#[GCC 4.6.3] on linux2
#Type "copyright", "credits" or "license()" for more information.
import datetime
import picamera
import numpy
import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from skimage import data
from skimage.feature import blob_doh, blob_log, blob_dog
from matplotlib import pyplot as plt
from matplotlib import patches as patch
from math import sqrt
from skimage.color import rgb2gray
from time import sleep, perf_counter
import math

def roundup(x):
        return int(math.ceil(x/5.0))*5

while True:
    print("start")
    #Names image to be saved with timestamp so it is unique
    tic=perf_counter()
    time_now=datetime.datetime.now()
    time_formatted=time_now.strftime("%Y-%m-%d_%H-%M-%S")
    image_name= "/home/pi/camera/{}.png".format(time_formatted)
    #image_name="/home/pi/red5.jpg"
     
    #Camera takes picture and saves its name as the time stamp
    print("taking picture")
    camera=picamera.PiCamera()
    sleep(2)

    camera.capture("{}".format(image_name))
    #Copies Image and resises it so processing is faster (reduces precision)
    img_orig=Image.open("{}".format(image_name))
    img=img_orig.copy()
    width_orig, height_orig= img.size
    reduction_factor=5
    width=roundup(width_orig/reduction_factor)
    height=roundup(height_orig/reduction_factor)
    print("picture resized")
    img=img.resize((width,height))
    img.save("{}".format(image_name))
    width, height= img.size
    print("width", width, "\nheight", height)

    #Converts from colored image to greyscale for easier processing
    image=data.imread(("{}".format(image_name)))
    image_gray=rgb2gray(image)
    camera.close()

    #Finds laser using difference of Hessian algorithm
    blobs_doh=blob_doh(image_gray, max_sigma=30, threshold=.01)#30,0.01

    #Plots circle of blob found on original image
    fig=plt.figure()
    ax=fig.add_subplot(111)
    plt.imshow(image, interpolation="nearest")
    for blob in blobs_doh:
        y,x,r= blob
        print("x-",x,"\ny-",y, "\nr-",r)
        circ=patch.Circle((x,y),r,color="black",linewidth=4, fill=False)
        ax.add_patch(circ)
        ax.text(x,y,"X", horizontalalignment="center",
                verticalalignment="center",
                fontsize=10,color="black")
    #Saves picture, ends timer
    image_edited_name= "/home/pi/camera/{}edited.png".format(time_formatted)
    fig.savefig(("{}".format(image_edited_name)))
    sleep(5)
    toc=perf_counter()
    total_time=toc-tic
    print("Total time:",total_time)
