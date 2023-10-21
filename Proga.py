import cv2
import mediapipe as mp
import time

qcap = cv2.VideoCapture(0) 
# cap = cv2.VideoCapture("Videos/1.mp4") 

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

pTime = 0
cTime = 0

def count_fingers(results):
    # The order of key points that are used for finger analysis
    finger_point_indices = [4, 8, 12, 16, 20]
    thumb_tip = results.right_hand_landmarks.landmark[4].y

    finger_count = 0
    for point_index in finger_point_indices:
        if results.right_hand_landmarks.landmark[point_index].y < thumb_tip:
            finger_count += 1
    return finger_count

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while qcap.isOpened():
        ret, frame = qcap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        # print(results.pose_landmarks)
        # print(results.left_hand_landmarks)
        # print(results.right_hand_landmarks)
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

        # Cut off a few fingers
        if results.right_hand_landmarks:
            finger_count = count_fingers(results)
            cv2.putText(image, f'Fingers: {finger_count}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
 

        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

qcap.release()
cv2.destroyAllWindows()
