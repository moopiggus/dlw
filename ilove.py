import cv2
import numpy as np
import time
import poseDetector as pd

cap = cv2.VideoCapture(0) # open webcam
detector = pd.poseDetector() # create poseDetector object
count = 0
pTime = 0

while True: 
    color = (255, 0, 255)
    success, img = cap.read()
    img = detector.drawSkeleton(img)
    lmList = detector.findPositions(img)
    if len(lmList) != 0:  
        if detector.findAngle(img, 11, 13, 15) < 150 :
            cv2.putText(img, "loveee <3", (1000, 800), 
                        cv2.FONT_HERSHEY_PLAIN, 10, color, 5)
        else:
            cv2.putText(img, "I", (1000, 800), 
                        cv2.FONT_HERSHEY_PLAIN, 10, color, 5)
            
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime # update prev time
    cv2.putText(img, str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    # display img in window named "ai form checker"
    cv2.imshow("AI Form Checker", img)
    # refresh window every millisecond until key press exits loop
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cap.destroyAllWindows()