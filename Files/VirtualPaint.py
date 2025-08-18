# Using necessary Libraries
import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

##########
brushThickness = 15
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
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    # Setting the header image
    img[0:125, 0:1280] = header 
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    