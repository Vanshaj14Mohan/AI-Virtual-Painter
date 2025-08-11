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

#Main Loop
while True:
    success, img = cap.read() # Read frame from webcam
    cv2.imshow("Image", img)
    cv2.waitKey(1)