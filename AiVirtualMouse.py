import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

#######################
wcam, hcam = 650,500
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
frame = 100  # frame reduction
smoothening = 7
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0
#######################


cap = cv2.VideoCapture(0)

while True:
    # 1
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1,y1,x2,y2)

        # 3 check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (80, 20), (wcam-frame, hcam-frame), (255,0,255), 2)

        # 4
        if fingers[1]==1 and fingers[2]==0:
            # 5
            x3 = np.interp(x1, (frame, wcam-frame), (0, wScr))
            y3 = np.interp(y1, (frame, hcam-frame), (0, hScr))

            # 6
            cLocX = pLocX + (x3 - pLocX) / smoothening
            cLocY = pLocY + (y3 - pLocY) / smoothening

            # 7
            autopy.mouse.move(wScr - cLocX, cLocY)
            cv2. circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
            pLocX, pLocY = cLocX, cLocY

        # 8
        if fingers[1]==1 and fingers[2]==1:
            # 9
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # 10
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
    # 11
    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 3)

    # 12
    cv2.imshow("Image", img)
    cv2.waitKey(1)