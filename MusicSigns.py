import time
import cv2
import HandTrackingModule as htm
from pygame import mixer

wCam, hCam = 1280, 800

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDectector(detectionCon=0.50)

tipIds = [4, 8, 12, 16, 20]
mixer.init()

pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)



    if len(lmList) != 0:
        fingers = []
        index_up = lmList[tipIds[1]][2] < lmList[tipIds[1]-2][2]
        middle_up = lmList[12][2] < lmList[10][2]
        ring_up = lmList[16][2] < lmList[14][2]
        pinky_up = lmList[20][2] < lmList[18][2]
        thumb_up = lmList[4][1] <= lmList[3][1]
        if index_up:
            if middle_up:
                if ring_up and not pinky_up and thumb_up:
                    signNumber=6
                elif pinky_up and not ring_up:
                    signNumber=7
                elif thumb_up:
                    if not ring_up:
                        signNumber=3
                    if ring_up and pinky_up:
                        signNumber=5
                elif ring_up:
                    if pinky_up:
                        signNumber=4
                else:
                    signNumber=2
            elif pinky_up and ring_up:
                signNumber=8
            else:
                signNumber=1
        elif pinky_up and ring_up and middle_up:
            signNumber=9
        elif thumb_up:
            signNumber=10
        else:
            signNumber=0


        if not mixer.music.get_busy():
            if signNumber == 1:
                mixer.music.load('c4.mp3')
                mixer.music.play()
            elif signNumber == 2:
                mixer.music.load('d4.mp3')
                mixer.music.play()
            elif signNumber == 3:
                mixer.music.load('e4.mp3')
                mixer.music.play()
            elif signNumber == 4:
                mixer.music.load('f4.mp3')
                mixer.music.play()
            elif signNumber == 5:
                mixer.music.load('g4.mp3')
                mixer.music.play()
            elif signNumber == 6:
                mixer.music.load('a4.mp3')
                mixer.music.play()
            elif signNumber == 7:
                mixer.music.load('b4.mp3')
                mixer.music.play()
            elif signNumber == 8:
                mixer.music.load('c5.mp3')
                mixer.music.play()
            elif signNumber == 9:
                mixer.music.load('d5.mp3')
                mixer.music.play()
            elif signNumber == 10:
                mixer.music.load('e5.mp3')
                mixer.music.play()

        cv2.rectangle(img, (15, 15), (260, 220), (200, 125, 0), cv2.FILLED)
        cv2.putText(img, str(signNumber), (50, 165), cv2.FONT_HERSHEY_PLAIN,
                    10, (0, 0, 0), 15)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #cv2.putText(img, str(int(fps)), (1150, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
