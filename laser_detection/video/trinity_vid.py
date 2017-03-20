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
from matplotlib import pyplot as plt
from matplotlib import patches as patch
from time import sleep
import cv2

def find_blob_coords (image_name,index,filename):


        #Finds laser using difference of Hessian algorithm
        print "index:{}".format(index)
        #Plots circle of blob found on original image
        im = cv2.imread(image_name)
        im =cv2.resize(im,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
        im =cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )
        im =cv2.GaussianBlur(im,(9,9),0)
        
        thresh = cv2.threshold(im, 200, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.erode(thresh, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=4)

        thresh
        imCopy = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB )
        contours, hierarchy= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)
        
        if len(contours)!=0:
                
                contour_areas = [cv2.contourArea(contour) for contour in contours]
                max_index = np.argmax(contour_areas)
                max_contour=contours[max_index]

                contour_moment = cv2.moments(max_contour)
                cx = int(contour_moment['m10']/contour_moment['m00'])
                cy = int(contour_moment['m01']/contour_moment['m00'])
####                (x,y),radius = cv2.minEnclosingCircle(max_contour)
####                center = (int(x),int(y))
####                radius = int(radius)
####                cv2.circle(imCopy,center,radius,(0,0,255),1)
####                print "Centre:({},{})".format(x,y)
####                print "radius: {}".format(radius)
##                cv2.drawContours(imCopy, max_contour, -1, (0,255,0), 1)
                print "blob found"
                cv2.imwrite(image_name,imCopy)
                return np.array([index,cx,cy])
        else:
                cv2.imwrite(image_name,imCopy)
                return []

        


tic= datetime.datetime.now()
while True:
    print("start")
    #Names image to be saved with timestamp so it is unique
    tic=datetime.datetime.now()
    time_now=datetime.datetime.now()
##    time_formatted=time_now.strftime("%Y-%m-%d_%H-%M-%S")
    time_formatted="redb3"
    
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
                if index_results!=[]:
                        results=np.vstack((results, index_results))
    #print"results {}".format(results)
    xy_coords=results[1:,1:]
    plt.figure()
    plt.scatter(xy_coords[0:,0],xy_coords[0:,1])
    plt.title("Laser Trajectory")
    plt.xlabel("x_coords")
    plt.ylabel("y_coords")
    plt.xlim(xmin=0)
    plt.ylim(ymin=0)
    plt.savefig("{}-trajectory.png".format(video_name))
    toc=datetime.datetime.now()
    programtime=toc-tic
    print"Time: {}".format(programtime.seconds)
    
    
