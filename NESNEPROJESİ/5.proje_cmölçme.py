import cv2
import numpy as np
cap = cv2.VideoCapture(0)
scale_factor = 2.0
point1 = None
point2 = None
distance_pixels = None
width_pixels = None
while True:
    ret, frame = cap.read()
    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([30, 30, 30], dtype=np.uint8)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_black, upper_black)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        point1 = np.array([x, y])
        point2 = np.array([x + w, y + h])
        distance_pixels = np.linalg.norm(point1 - point2)
        width_pixels = abs(point1[0] - point2[0])
        distance_real_world = distance_pixels * scale_factor
        width_real_world = width_pixels * scale_factor
        cv2.putText(frame, f"Distance: {distance_real_world:.2f} units", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Width: {width_real_world:.2f} units", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
