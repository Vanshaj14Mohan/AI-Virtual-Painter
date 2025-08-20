# Using necessary Libraries
import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

##########
brushThickness = 15
eraserThickness = 80
##########

# Load images from folder
folderPath = "PaintImage"
myList = os.listdir(folderPath) # List all image filenames in the folder
print(myList)

overlayList = [] # List to store loaded images
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}') # Read each image
    overlayList.append(image) # Add to the overlay list

print("The length of images are:",len(overlayList)) # Print how many images were loaded
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.HandDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# Main Loop
while True:
    # 1: Import image
    success, img = cap.read() # Read frame from webcam
    img = cv2.flip(img,1)

    # 2: Finding Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList)  
        #Tip of index and middle fingers
        x1,y1 = lmList[8][1:] #For index finger
        x2,y2 = lmList[12][1:] #For middle finger
        
        # 3: Checking which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4: Selection mode - If two fingers are up
        if fingers[1] and fingers[2]:
            # cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)
            xp, yp = 0, 0
            print("Selection Mode")
            #Checking the click condition now
            if y1 < 125:
                if 250< x1<450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255) # For Purple color
                elif 550< x1<750:
                    header = overlayList[1]
                    drawColor = (0, 165, 255) # For Orange color
                elif 800< x1<950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0 ) # For Green color
                elif 1050< x1<1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0 ) # For Black color
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)
    
        # 5: Drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0: #Condition
                xp, yp = x1, y1
            
            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)          

            # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            # cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image
    img[0:125, 0:1280] = header 
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inverse Image", imgInv)
    cv2.waitKey(1)

    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    