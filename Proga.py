import cv2
import numpy as np
import mediapipe as mp
import time
import os

# cap = cv2.VideoCapture(0) 
cap = cv2.VideoCapture("Videos/1.mp4") 
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True: 
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        # print(results.right_hand_landmarks)
        # print(results.left_hand_landmarks)
        # print(results.pose_landmarks)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Pose Detections
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(image, str(int(fps)),(10,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    
    cv2.imshow('python', image)
    if cv2.waitKey(20) == 27:
        break
        
cv2.destroyWindow("python")
cap.release()
cv2.waitKey(1)
