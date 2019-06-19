import urllib.request
import cv2
import numpy as np
url='http://192.168.43.57:8080/shot.jpg'

success = 1
while success: 
        # vidObj object calls read 
        # function extract frames 
        imgResp = urllib.request.urlopen(url)
    
    # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    
    # Finally decode the array to OpenCV usable format ;) 
        image = cv2.imdecode(imgNp,-1)
        font = cv2.FONT_HERSHEY_COMPLEX
        blur=cv2.blur(image,(15,15))
        img = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
        morphed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        contours, _=cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contor = sorted(contours, key=cv2.contourArea)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            cv2.drawContours(image, [approx], 0, (50, 205, 50), 5)
            if len(approx) == 3:
                cv2.putText(image, "Triangle", (x, y), font, 1, (0))
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx) 
                ar = w / float(h)
                cv2.putText(image, "Square", (x, y), font, 1, (0)) if ar >= 0.95 and ar <= 1.05 else cv2.putText(image, "Rectangle", (x, y), font, 1, (0))
            elif len(approx) == 5:
                cv2.putText(image, "Pentagon", (x, y), font, 1, (0))
            elif len(approx) == 6:
                cv2.putText(image, "Hexagon", (x, y), font, 1, (0))
            elif len(approx) == 7:
                cv2.putText(image, "Septagon", (x, y), font, 1, (0))
            elif len(approx) == 8:
                cv2.putText(image, "Octagon", (x, y), font, 1, (0))
            elif 8 < len(approx) < 15:
                cv2.putText(image, "Ellipse", (x, y), font, 1, (0))
            else:
                cv2.putText(image, "Circle", (x, y), font, 1, (0))
        cv2.imshow("shapes", image)
        cv2.imshow("Threshold", threshold)
        key = cv2.waitKey(5) & 0xFF
        if key == ord('s'):
            break
cv2.destroyAllWindows()