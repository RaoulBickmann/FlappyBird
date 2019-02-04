import cv2
import sys
import numpy as np
import pandas as pd
import KalmanFilter as kf
import UtilityFunctions as uf
 
def analyseImage():  
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    #if int(minor_ver) < 3:
    #    tracker = cv2.Tracker_create(tracker_type)
    #else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
        atracker = cv2.TrackerCSRT_create()
 
    # Read video
    video = cv2.VideoCapture("movie_movie2.mov")
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
    abox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    abox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    ok = atracker.init(frame, abox)
    counter = 0;
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
        ok, abox = atracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))    
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            
            a1 = (int(abox[0]), int(abox[1]))
            a2 = (int(abox[0] + abox[2]), int(abox[1] + abox[3]))
            cv2.rectangle(frame, a1, a2, (0,0,255), 2, 1)

            m1 = int((p1[0] + p2[0]) / 2)
            m2 = int((a1[0] + a2[0]) / 2)

            print(str(counter) + ": " + str(m1) + " : " + str(int(p1[1] + p2[1]) / 2))
            counter = counter + 1
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break


def colorAnalyse():

    # Read video
    video = cv2.VideoCapture("movie_movie5.mov")
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
 
    outdata = pd.DataFrame(columns=['cm'])

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
 
        if ok:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_green = np.array([70,80,140])
            upper_green = np.array([100,255,255])
            

            mask = cv2.inRange(hsv, lower_green, upper_green)
            res = cv2.bitwise_and(frame,frame, mask= mask)

            x = 850
            y = 150
            while True:
                px = mask[y, x]
                if(px == 255):
                    cm = -1 * ((x - 915) / (30 + np.abs(1- x / 450)))
                    #print((30 + np.abs(1- x / 450)))
                    outdata = outdata.append({'cm': np.round(cm, 4)}, ignore_index = True)
                    break
                x = x - 1
            
            cv2.circle(frame, (x, y), 10, (255,0,0), -1)
            

            #cv2.imshow('frame',frame)
            #cv2.imshow('mask',mask)
            #cv2.imshow('res',res)

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

    outdata.to_csv('camera_truth_cm2.csv', index=False, sep=';')




def drawData():
    data = pd.read_csv('data_movie5.csv')
    y = np.array(data.cm)
    N = len(data.cm)
    Ts = 0.02
    t = data.time

    x, P = kf.filter(y, N, Ts)

    # Read video
    video = cv2.VideoCapture("movie_movie5.mov")
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
     
    counter = 0
    n = 0
    width = video.get(3)  # float
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
 
        # Draw bounding box
        if ok:
            if(n == len(data.cm)):
                break

            if(counter > 445):
                cm = -1 * ((x - 915) / (30 + np.abs(1- x / 450)))

                cv2.circle(frame, (int(x[n][0] * -(30) + 915), 300), 10, (255,0,0), -1)
                cv2.circle(frame, (int(data.cm[n] * -(30) + 915), 277), 10, (0,0,255), -1)
                n = n + 1

            counter = counter + 1

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 

        # Display result
        cv2.imshow("Tracking", frame)


 
        # Exit if ESC pressed
        k = cv2.waitKey(15) & 0xff
        if k == 27 : break


def findCM():
    # Read video
    video = cv2.VideoCapture("movie_movie5.mov")
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
 
        if ok:
            
            x = 915
            y = 330
            while (x > 0):
                cv2.circle(frame, (x, y), 3, (255,0,0), -1)
                x = x - 30

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(15) & 0xff
        if k == 27 : break
