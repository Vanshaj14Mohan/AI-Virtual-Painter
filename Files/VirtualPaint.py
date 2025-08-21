import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm  

########## CONFIGURATION ##########
brushThickness = 15      # Thickness of the brush for drawing
eraserThickness = 80     # Thickness of the eraser
###################################

# Load header images (used as color selection menu)
folderPath = "PaintImage"
myList = os.listdir(folderPath)  # List of all files inside PaintImage folder
print(myList)

overlayList = []  # Store loaded images
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')  # Read image
    overlayList.append(image)                     # Add to list

print("The length of images are:", len(overlayList))  # Debug: how many images loaded

header = overlayList[0]         # Default header (first image)
drawColor = (255, 0, 255)       # Default color: Purple (BGR format)

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)   # Width of video frame
cap.set(4, 720)    # Height of video frame

# Initialize hand detector
detector = htm.HandDetector(detectionCon=0.85)

xp, yp = 0, 0   # Previous point coordinates (for drawing lines)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Transparent canvas for drawing

# ----------------- MAIN LOOP -----------------
while True:
    # 1: Import image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip horizontally for natural interaction

    # 2: Detect hands and landmarks
    img = detector.findHands(img)                     # Draw landmarks on hand
    lmList = detector.findPosition(img, draw=False)   # Get landmark positions

    if len(lmList) != 0:   # If hand landmarks detected
        # Tip coordinates of index and middle fingers
        x1, y1 = lmList[8][1:]   # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip

        # 3: Detect which fingers are up
        fingers = detector.fingersUp()

        # 4: Selection mode (when two fingers are up → index + middle)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0   # Reset previous points
            print("Selection Mode")

            # Check if finger is in header region (y < 125 pixels)
            if y1 < 125:
                # Choose different tools/colors depending on x-position
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)   # Purple
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (0, 165, 255)   # Orange
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)     # Green
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)       # Black (Eraser)

            # Draw selection rectangle
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5: Drawing mode (only index finger up)
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)   # Show pointer
            print("Drawing Mode")

            # First frame → just store starting point
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Eraser mode (black color chosen)
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)   # Erase on live feed
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness) # Erase on canvas
            else:
                # Draw colored line
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            # Update previous points
            xp, yp = x1, y1

    # 6: Merge canvas and webcam feed
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)   # Convert canvas to grayscale
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)  # Invert
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)   # Mask out drawing area
    img = cv2.bitwise_or(img, imgCanvas) # Combine canvas with live feed

    # 7: Overlay the header (color selection toolbar)
    img[0:125, 0:1280] = header

    # Display windows
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    