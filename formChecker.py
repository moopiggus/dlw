import cv2
import numpy as np
import time
import poseDetector as pd

cap = cv2.VideoCapture(0) # open webcam
detector = pd.poseDetector() # create poseDetector object
count = 0
dir = 0 # starts from moving upwards
pTime = 0

low_angle = 30
high_angle = 160

while True:
    success, img = cap.read()
    img = detector.drawSkeleton(img)
    lmList = detector.findPositions(img)
    if len(lmList) != 0:
        angle = detector.findAngle(img, 11, 13, 15) # I only want to see the 3 joints, draw=True is default
        # scale to percentage
        per = np.interp(angle, (low_angle, high_angle), (100, 0))
        # bar represents progress in exercise
        # progress indicator that moves up or down depending on detected joint angle
        # help users see if full motion completedjm
        bar = np.interp(angle, (low_angle, high_angle), (100, 650))
        # check the dumbbell curl
        # fix lack of discipline later
        color = (255, 0, 255)
        if per == 100:
            if dir == 0: # going up
                count += 0.5
                dir = 1 # change to going down
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        # Draw progress bar
        # border
        cv2.rectangle(img, (1700, 100), (1775, 650), color, 1)
        # fill with colour based on per
        cv2.rectangle(img, (1700, int(bar)), (1775, 650), color, cv2.FILLED)
        cv2.putText(img, str(int(per)) + '%', (1680, 75), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)

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

