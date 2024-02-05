from cvzone.HandTrackingModule import HandDetector
import cv2
import math
import numpy as np
import cvzone
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=False)
    if hands:
        for hand in hands:
            lmList = hand['lmList']
            x, y, w, h = hand['bbox']
            x1, y1, _ = lmList[8]  
            x2, y2, _ = lmList[12]  
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            distanceCM = A * distance ** 2 + B * distance + C
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))
    key = cv2.waitKey(1)
    if key == 27:
        break
    cv2.imshow("Image", img)
    cv2.waitKey(1)



