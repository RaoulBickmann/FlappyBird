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


def drawData():
    data = pd.read_csv('data_movie2.csv')
    y = np.array(data.cm)
    N = len(data.cm)
    Ts = 0.02
    t = data.time

    y = uf.preFilter2(y)

    x, P = kf.filter(y, N, Ts)

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
     
    counter = 0
    n = 0
    width = video.get(3)  # float
    offset = 3850
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
 
        # Draw bounding box
        if ok:
            if(counter * 33.333 > offset):
                while(data.time[n] + offset < counter * 33.333):
                    n = n + 1

                cv2.circle(frame, (int(width - x[n][0] * 53 - 400), 300), 10, (255,0,0), -1)
                cv2.circle(frame, (int(width - data.cm[n] * 53 - 400), 277), 10, (0,0,255), -1)

            counter = counter + 1

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 

        # Display result
        cv2.imshow("Tracking", frame)


 
        # Exit if ESC pressed
        k = cv2.waitKey(30) & 0xff
        if k == 27 : break