import numpy as np
import time
import imutils
import cv2

avg = None

# IP Kamera bağlantısı için
video = cv2.VideoCapture('rtsp://10.31.125.7:8080/h264_pcm.sdp')


video = cv2.VideoCapture("insan2.mp4")

fourcc=cv2.VideoWriter_fourcc(*'XVID')
out =cv2.VideoWriter('output.avi',fourcc, 25.00, (640,480))


#width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)  #Alınan video nun genisligi  
#height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5) # Alınan video nun uzunluğu

#size = (width, height)
#print(size)

#out = cv2.VideoWriter('output.avi',-1, 20.0, (640,480))


#camera_A=cv2.VideoCapture("askdfasdfsad")

"""
camera_b=cv2.VideoCapture(1)
camera_c=cv2.VideoCapture(2)
camera_d=cv2.VideoCapture(3)
camera_e=cv2.VideoCapture(4)
camera_f=cv2.VideoCapture(5)
camera_g=cv2.VideoCapture(6) """

    
xvalues = list()
motion = list()
giris = 0
cikis = 0
def find_majority(k):
    myMap = {}
    maximum = ( '', 0 ) # meydana gelen eleman, oluşumlar
    for n in k:
        if n in myMap: myMap[n] += 1
        else: myMap[n] = 1

        # Hareket halindeyken maksimum tutarı takip edin
        if myMap[n] > maximum[1]: maximum = (n,myMap[n])

    return maximum

while True:
    #ret, frame_A =camera_A.read()
    ret, frame = video.read()
   # frame= cv2.flip(frame,180)  #Döndürülmüş çerçeve 180 derece dönderme işlemi
    
    flag = True
    text=""
 #   camera_A=imutils.resize(frame_A, width=600)
    #frame = imutils.resize(frame, width=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if avg is None:
        print ( "Video goruntuleri baslatiliyor")
        avg = gray.copy().astype("float")
        continue

    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in cnts:
        if cv2.contourArea(c) < 5000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        xvalues.append(x)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        flag = False
	
    no_x = len(xvalues)
    
    if (no_x > 2):
        difference = xvalues[no_x - 1] - xvalues[no_x - 2]
        if(difference > 0):
            motion.append(1)
        else:
            motion.append(0)

    if flag is True:
        if (no_x > 5):
            val, times = find_majority(motion)
            if val == 1 and times >= 15:
                giris += 1
            else:
                cikis += 1
                
        xvalues = list()
        motion = list()
    
    #cv2.line(frame, (290, 160), (490,160), (0,255,0), 2) # insan1.mp4 için line çizgisi
    
    cv2.line(frame, (260, 0), (260,480), (0,255,0), 2)
    cv2.line(frame, (420, 0), (420,480), (0,255,0), 2)
    #cv2.putText(frame_A, "Giris: {}".format(giris), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)	
    
    cv2.putText(frame, "Giris: {}".format(giris), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #print("x:{}".format(giris))
    cv2.putText(frame, "Cikis: {}".format(cikis), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #print("y:{}".format(cikis))
    
    cv2.imshow("Video",frame)
    
    
    out.write(frame)
    # cv2.imshow("Camera A",frame_A)
    #cv2.imshow("GRI",gray)
    #cv2.imshow("FrameDelta",frameDelta)
    
#    out=cv2.VideoWriter("insan2.mp4",frame)
  
        
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

video.release()
    
out.release()
#camera_A.release()
cv2.destroyAllWindows()
