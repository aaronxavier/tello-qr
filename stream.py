#!/usr/bin/python3

"""
@brief      This is program for streaming video from Tello camera and detect ArUco markers in the feed.
@author     Aaron Xavier
@date       08-May-2025
"""

import threading
import socket
import cv2
import numpy as np


""" Welcome note """
print("\nTello Video Stream Program\n")


class Tello:
    def __init__(self):
        self._running = True
        self.video = cv2.VideoCapture("udp://@0.0.0.0:11111")
        # Initialize ArUco dictionary and parameters
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.aruco_detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        # Initialize detection counter
        self.detection_count = 0
        self.last_detected_ids = set()

    def terminate(self):
        self._running = False
        self.video.release()
        cv2.destroyAllWindows()

    def readAruco(self, frame):
        """Detect ArUco markers in the frame"""
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect markers
        corners, ids, rejected = self.aruco_detector.detectMarkers(gray)
        
        # Draw detected markers and update counter
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Get current detected IDs
            current_ids = {id[0] for id in ids}
            
            # Count new detections (IDs not seen in previous frame)
            new_detections = current_ids - self.last_detected_ids
            self.detection_count += len(new_detections)
            
            # Update last detected IDs
            self.last_detected_ids = current_ids
            
            # Print marker IDs and total count
            for i in range(len(ids)):
                print(f"Detected ArUco marker ID: {ids[i][0]}")
            print(f"Total detections: {self.detection_count}")
            
            # Display count on frame
            cv2.putText(frame, f"Detections: {self.detection_count}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
        return frame

    def recv(self):
        """ Handler for Tello states message """
        while self._running:
            try:
                ret, frame = self.video.read()
                if ret:
                    # Resize frame
                    height, width, _ = frame.shape
                    new_h = int(height / 2)
                    new_w = int(width / 2)

                    # Resize for improved performance
                    new_frame = cv2.resize(frame, (new_w, new_h))
                    
                    # Process frame for ArUco detection
                    new_frame = self.readAruco(new_frame)

                    # Display the resulting frame
                    cv2.imshow('Tello', new_frame)
                # Wait for display image frame
                # cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.waitKey(1)
            except Exception as err:
                print(err)


""" Start new thread for receive Tello response message """
t = Tello()
recvThread = threading.Thread(target=t.recv)
recvThread.start()

while True:
    try:
        # Get input from CLI
        msg = input()

        # Check for "end"
        if msg == "bye":
            t.terminate()
            recvThread.join()
            print("\nGood Bye\n")
            break
    except KeyboardInterrupt:
        t.terminate()
        recvThread.join()
        break
