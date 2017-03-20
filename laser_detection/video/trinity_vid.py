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

def clean_image (image):
        image =cv2.GaussianBlur(image,(9,9),0)          
        thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=2)
        im_clean = thresh

        return im_clean
def find_first_blob_coords(contours,imCopy):
        contour_areas = [cv2.contourArea(contour) for contour in contours]
        max_index = np.argmax(contour_areas)
        max_contour=contours[max_index]

        contour_moment = cv2.moments(max_contour)
        cx = (contour_moment['m10']/contour_moment['m00'])
        cy = (contour_moment['m01']/contour_moment['m00'])
##        (x,y),radius = cv2.minEnclosingCircle(max_contour)
##        center = (int(x),int(y))
##        radius = int(radius)
##        cv2.circle(imCopy,center,radius,(0,0,255),1)
##        cv2.drawContours(imCopy, max_contour, -1, (0,255,0), 1)

        return cx, cy
        
def find_blob_coords (frame,index,video_name):
        
        global cx, cy, blob_found, radius, height, width
        #Load Image, Resize and Convert To Grayscale
        im = frame
        image_name="{}-index{}cleaned.png".format(video_name,index)
        #im_name="{}-index{}.png".format(video_name,index)
        #im =cv2.resize(im,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
        height, width, channels = im.shape
        im =cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )
        #cv2.imwrite(im_name,im)
        
        if blob_found==True:
                #If Blob found in Previous Frame
                #Set Region of Interest (roi) to look for blob in frame
                xmin = max(0,cx-20)
                ymin = max(0,cy-20)
                xmax = min(width, cx +20)
                ymax = min(height, cy+20)

                roi = im[ymin:ymax,
                        xmin:xmax]
                thresh = clean_image (roi)
                imCopy = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
                contours, hierarchy= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_NONE)
                
                if len(contours)!=0:
                        cropped_cx, cropped_cy= find_first_blob_coords(contours, imCopy)
                        cx = cropped_cx+ xmin
                        cy = cropped_cy+ ymin
                        blob_found=True
                        return np.array([index,cx,cy])
                else:
                        #cv2.imwrite(image_name,roi)#Change im to roi for troubleshooting
                        blob_found=False
                        print "no blob found in cropped frame #{}".format(index)
                        return []

        else:
                #If Blob not found in Previous Frame
                #searches whole image rather than ROI
                thresh = clean_image (im)
                imCopy = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB )
                contours, hierarchy= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_NONE)
                
                if len(contours)!=0:                  
                        cx, cy= find_first_blob_coords(contours, imCopy)
                        #cv2.imwrite(image_name,imCopy)
                        blob_found=True
                        return np.array([index,cx,cy])
                else:
                        #cv2.imwrite(image_name,im)
                        blob_found=False
                        print "no blob found in frame #{}".format(index)
                        return []
def plot_trajectory(xy_coords):
        global index, height, width
        plt.figure()
        #plt.axis((0,width,0,height))
        plt.scatter(xy_coords[0:,0],xy_coords[0:,1])
        numberOfBlobsDetected=xy_coords[0:,0].size
        plt.title("Laser Trajectory-{}/{}blobs found".format(numberOfBlobsDetected
                                                                 ,index))
        plt.xlabel("x_coords")
        plt.ylabel("y_coords")
##        plt.xlim(xmin=0)
##        plt.ylim(ymin=0)
        plt.savefig("{}-trajectory.png".format(video_name))
def trajectory_analysis(results):
        
        frame_no=results[1:,0]
        #time= frame_no/5
        x_coords=results[1:,1]
        y_coords=results[1:,2]
        plt.close('all')

        fig, axarr = plt.subplots(2, sharex=True)

        axarr[0].plot(frame_no, x_coords)
        axarr[0].set_title("Trajectory Coordinates vs Frame Number")
        axarr[0].set_xlabel("Frame Number")
        axarr[0].set_ylabel("x coordinate")
        axarr[1].set_xlabel("Frame Number")
        axarr[1].set_ylabel("y coordinate")
        axarr[1].plot(frame_no, y_coords)

        fig.savefig("{}_analysis.png".format(video_name))
                            
tic= datetime.datetime.now()
while True:
    print("start")
    #Initialise Variables to be used by functions
    blob_found=False
    cx=cy=radius=index=height=width=0
    #Names image to be saved with timestamp so it is unique
    tic=datetime.datetime.now()
    time_now=datetime.datetime.now()
##    time_formatted=time_now.strftime("%Y-%m-%d_%H-%M-%S")
    #time_formatted="2V_1Hz_10cm_1640x1232"
    time_formatted="fixed_vertical_2V"
    
    video_name= "/home/pi/camera/{}".format(time_formatted)
    video_name_h264= "{}.h264".format(video_name)
    video_name_mp4= "{}.mp4".format(video_name)
    video_name_txt= "{}.txt".format(video_name)
    #Camera takes picture and saves its name as the time stamp
    print("taking video")
    with picamera.PiCamera() as camera:
        camera.resolution=(1640,1232)
        camera.framerate= 30
        camera.start_recording("{}".format(video_name_h264))
        camera.wait_recording(5)
        camera.stop_recording()
    #convert h264 to mp4 using gpac wrapper so it can be watched on PC/Mac
##    call("MP4Box -fps 30 -add {} {}".format(video_name_h264,video_name_mp4),shell=True)


    #Loads Video

    #vid = cv2.VideoCapture(video_name_mp4)
    vid = cv2.VideoCapture(video_name_h264)
    results=np.array(["index","x-coord","y-coord"])

    #Check if Video was Loaded Properly
    if not vid.isOpened():
            print "can't open video"
    #Iterates through each video frame and finds blob
    while(vid.isOpened()):
            index=index+ 1
            ret, frame = vid.read()     
            if ret==True:
                frame=cv2.flip(frame,0)
                index_results=find_blob_coords(frame,index,video_name)
                if index_results!=[]:
                        results=np.vstack((results, index_results))
            else:
                    break
    print"results {}".format(results)
    np.savetxt(video_name_txt,results, delimiter="  ", fmt="%s")

    xy_coords=results[1:,1:]
    plot_trajectory(xy_coords)
    trajectory_analysis(results)
    toc=datetime.datetime.now()
    programtime=toc-tic
    print"Time: {}".format(programtime.seconds)
    print "sleeping for 30 secs"
    sleep(30)
    
    

