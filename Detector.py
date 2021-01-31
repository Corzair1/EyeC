import cv2 as cv
import numpy as np
from urllib.request import urlopen
import os
import datetime
import time
import sys

#change to your ESP32-CAM ip
url="http://192.168.31.184:81/stream"
CAMERA_BUFFRER_SIZE=4096
stream=urlopen(url)
bts=b''
while True:
    try:
        while True:
            bts+=stream.read(CAMERA_BUFFRER_SIZE)
            jpghead=bts.find(b'\xff\xd8')
            jpgend=bts.find(b'\xff\xd9')
            if jpghead>-1 and jpgend>-1:
                jpg=bts[jpghead:jpgend+2]
                bts=bts[jpgend+2:]
                img=cv.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv.IMREAD_UNCHANGED)
                v=cv.flip(img,0)
                h=cv.flip(img,1)
                p=cv.flip(img,-1)        
                frame=p
                img=cv.resize(frame,(480,320))

                img = img[0:200, 60:300]

                h, w = img.shape[:2]

                
                img = cv.rotate(img, cv.cv2.ROTATE_90_CLOCKWISE)

                rows, cols, _ = img.shape

                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                gray_img = cv.GaussianBlur(gray_img, (7, 7), 0)

                

                _, threshold = cv.threshold(gray_img, 70, 255, cv.THRESH_BINARY_INV)

                contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                contours = [max(contours, key = cv.contourArea)]

                for c in contours:
                    M = cv.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # draw the contour and center of the shape on the image
                    cv.circle(gray_img, (cX, cY), 7, (255, 255, 255), -1)
                    cv.putText(gray_img, "center", (cX - 20, cY - 20),
                        cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


                #gray_img = cv.drawContours(gray_img, contours, -1, (0,255,0), 3)

                
            
                cv.imshow('contoured', gray_img)





            k=cv.waitKey(1)
            if k & 0xFF==ord('q'):
                exit()
        cv.destroyAllWindows() 
    except Exception as e:
        pass