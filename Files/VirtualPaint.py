# Using necessary Libraries
import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

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

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetector(detectionCon=0.85)

#Main Loop
while True:
    # 1: Import image
    success, img = cap.read() # Read frame from webcam
    img = cv2.flip(img,1)

    # 2: Finding Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        print(lmList)
        
        #Tip of index and middle fingers
        x1,y1 = lmList[8][1:] #For index finger
        x2,y2 = lmList[12][1:] #For middle finger

    # 3: Checking which fingers are up

    # 4: Selection mode - If two fingers are up

    # 5: Drawing mode - Index finger is up

    img[0:125, 0:1280] = header #Setting the header image
    cv2.imshow("Image", img)
    cv2.waitKey(1)




    # Break loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    