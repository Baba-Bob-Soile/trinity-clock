#Python 3.2.3 (default, Mar  1 2013, 11:53:50) 
#[GCC 4.6.3] on linux2
#Type "copyright", "credits" or "license()" for more information.
import os
from subprocess import call
import datetime
import picamera
import numpy as np
import imageio
import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from skimage import data
from skimage.feature import blob_doh, blob_log, blob_dog
from matplotlib import pyplot as plt
from matplotlib import patches as patch
from math import sqrt
from skimage.color import rgb2gray
from time import sleep
import math
from SimpleCV import Image, Color
import cv2

def roundup(x):
        return int(math.ceil(x/5.0))*5
def find_blob_coords (image_name,index,filename):

        print "index:{}".format(index)
        img = cv2.imread(image_name)
        orig = img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        radius=11
        gray = cv2.GaussianBlur(gray, (radius,radius), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        img = orig.copy()
        img=cv2.circle(img, maxLoc, radius, (255, 0, 0), 2)
 
        # display the results of our newly improved method
        cv2.imwrite(image_name, img)
        ##        if blobs:
##                circles = blobs.filter([b.isCircle(0.2) for b in blobs])
##                for b in circles:
##                        print b
##                        print "radius:{}".format(b.radius())
##                        print "centre:({}, {})".format(b.x,b.y)
##                
##                if circles:
##                        print ("found blob at index {}".format(index))
##                        
##			img.drawCircle((circles[-1].x, circles[-1].y),
##                                       circles[-1].radius(),
##                                       Color.BLUE,3)
##                        img.save()
##                        xmax=circles[-1].x
##                        ymax=circles[-1].y
##                        return np.array([index,xmax,ymax])
##                else:
##                        return []
##        else:
##                plt.clf()
##                return []

tic= datetime.datetime.now()
while True:
    print("start")
    #Names image to be saved with timestamp so it is unique
    tic=datetime.datetime.now()
    time_now=datetime.datetime.now()
##    time_formatted=time_now.strftime("%Y-%m-%d_%H-%M-%S")
    time_formatted="red7"
    
    video_name= "/home/pi/camera/{}".format(time_formatted)
    video_name_h264= "{}.h264".format(video_name)
    video_name_mp4= "{}.mp4".format(video_name)
    #Camera takes picture and saves its name as the time stamp
    print("taking picture")
##    with picamera.PiCamera() as camera:
##        camera.resolution=(640,480)
##        camera.start_recording("{}".format(video_name_h264))
##        camera.wait_recording(5)
##        camera.stop_recording()
    #convert to mp4 using gpac wrapper
##call("MP4Box -fps 30 -add {} {}".format(video_name_h264,video_name_mp4),shell=True)
    #Remove h264 file to save memory
#Line removed ASCII errror
    vid=imageio.get_reader(video_name_mp4)
    
    results=np.array(["index","x-coord","y-coord"])
    
    for index, im in enumerate (vid):
                img = vid.get_data(index)
                fig=plt.imshow(img)
                plt.axis("off")
                image_name="{}-index{}.png".format(video_name,index)
                fig.axes.get_xaxis().set_visible(False)
                fig.axes.get_yaxis().set_visible(False)
                
                plt.savefig("{}".format(image_name), bbox_inches="tight", pad_inches=0)
                plt.clf()
                index_results=find_blob_coords(image_name,index,video_name)
##                if index_results!=[]:
##                        results=np.vstack((results, index_results))
##    print"results {}".format(results)
##    xy_coords=results[1:,1:]
##    plt.figure()
##    plt.scatter(xy_coords[0:,0],xy_coords[0:,1])
##    plt.title("Laser Trajectory")
##    plt.xlabel("x_coords")
##    plt.ylabel("y_coords")
##    plt.xlim(xmin=0)
##    plt.ylim(ymin=0)
##    plt.savefig("{}-trajectory.png".format(video_name))
##    toc=datetime.datetime.now()
##    programtime=toc-tic()
##    print"Time: {}".format(programtime.seconds)
##    
    

