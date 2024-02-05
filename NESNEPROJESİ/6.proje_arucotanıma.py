import cv2
import cv2.aruco as aruco
import numpy as np
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
cap = cv2.VideoCapture(0)
scale_factor = 2.0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict)
    aruco.drawDetectedMarkers(frame, corners, ids)
    if ids is not None and len(ids) == 2:
        corner1 = corners[0][0][0]
        corner2 = corners[0][0][1]
        corner3 = corners[1][0][2]
        corner4 = corners[1][0][3]
        distance_pixels = np.linalg.norm(corner1 - corner3)
        distance_real_world = distance_pixels * scale_factor
        cv2.putText(frame, f"Distance: {distance_real_world:.2f} units", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
