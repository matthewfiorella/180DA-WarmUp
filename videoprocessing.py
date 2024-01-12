import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerBlueHsv = np.array([100,50,50])
    upperBlueHsv = np.array([120,255,255])
    mask = cv2.inRange(hsv, lowerBlueHsv, upperBlueHsv)
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    if contours:
        cnt = contours[0]
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()