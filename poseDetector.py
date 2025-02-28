import cv2
import mediapipe as mp
import math

class poseDetector() :

    def __init__(self):
        # load pose estimation model
        self.mpPose = mp.solutions.pose
        # initialise pose estimation object
        self.pose = self.mpPose.Pose(static_image_mode=False,
                                     min_detection_confidence=0.5,
                                     min_tracking_confidence=0.5,
                                     model_complexity=1)
        self.lmList = []
        self.mpDraw = mp.solutions.drawing_utils

    def drawSkeleton(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # enter img into pose model, runs pose estimation on img, stores key landmarks in results 
        self.results = self.pose.process(imgRGB)
        # return NormalizedLandmarkList (mediapipe object) of 33 NormalizedLandmark objects (fixed order of body parts)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            # predefined set of connections between key body points
        return img 

    def findPositions(self, img, draw=True):
        # landmark list
        self.lmList = []
        if self.results.pose_landmarks:
            # .landmark is list of normalizedlandmarks
            # enumerate returns iterable of pairs of index and value
            # use enumerate to store landmarks in same fixed order of body parts
            for id, lm in enumerate(self.results.pose_landmarks.landmark): 
                h, w, c = img.shape # returns dimensions of image
                cx, cy = int(lm.x*w), int(lm.y*h) # x and y coordinates of landmark
                self.lmList.append([id, cx, cy]) # append id, x, y to lmList, lmList is list of lists
                # make all joint cricle blue
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    # p123 are landmark indexes that you want
    def findAngle(self, img, p1, p2, p3, draw=True):
        _, x1, y1 = self.lmList[p1]
        _, x2, y2 = self.lmList[p2]
        _, x3, y3 = self.lmList[p3]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        angle =abs(angle)

        if angle > 180:
            angle = 360 - angle

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 3)
            # makes these 3 joints circle green
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            # label angle
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        return angle
