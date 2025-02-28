import cv2
import numpy as np
import time
import poseDetector as pd

cap = cv2.VideoCapture(0) # open webcam
detector = pd.poseDetector() # create poseDetector object
count = 0
dir = 1 # starts from moving downwards
pTime = 0


low_angle = 30
high_angle = 160

while True:
    success, img = cap.read()
    img = detector.drawSkeleton(img)
    lmList = detector.findPositions(img)
    color = (255, 0, 255)
    if len(lmList) != 0:
        if detector.findXDist(img, 12, 28) > 50 or detector.findXDist(img, 11, 27) > 50: 
            cv2.putText(img, "incorrect form! feet should be shoulder width apart", (1000, 675), 
                cv2.FONT_HERSHEY_PLAIN, 3, color, 2)
        if detector.findYDist(img, 24, 26) < 90 and dir == 1:
            count +=1
            dir = 0
            cv2.putText(img, "good job! <3", (1000, 675), 
                        cv2.FONT_HERSHEY_PLAIN, 3, color, 2)
        if detector.findYDist(img, 24, 26) > 200 and dir == 0:
            dir = 1
        if detector.findYDist(img, 24, 26) < 100: 
            cv2.putText(img, "good job! <3", (1000, 675), 
                        cv2.FONT_HERSHEY_PLAIN, 3, color, 2)
            
        # Display rep count
        # rectangle box
        cv2.rectangle(img, (0, 400), (160, 520), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(count)), (15, 500), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5)

    # Display FPS, show how smoothly ai model is running
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

