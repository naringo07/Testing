'''
DBFindColor.py - Allows user to find the color
that can be used for range tracking.  Use:
7,u,j,m - To adjust Hue
8,i,k,, - to adjust Saturation
9,o,l,. - to adjust Value

(c)2022. Brett Huffman
v.02
---------------------------------------
'''
from libs.DroneBLib import DroneB
from libs.DroneBLib import exiting, current_frame
import cv2
import numpy as np
import imutils

ihighH = 180
ilowH = 52
ihighS = 255
ilowS = 94
ihighV = 130
ilowV = 30

def main():


    db = DroneB()
    db.start(custom_loop = True)

    # Setup some special keyboard handlers
    db.controls["7"] = hh_up
    db.controls["u"] = hh_down
    db.controls["j"] = hl_up
    db.controls["m"] = hl_down
    db.controls["8"] = sh_up
    db.controls["i"] = sh_down
    db.controls["k"] = sl_up
    db.controls[","] = sl_down
    db.controls["9"] = vh_up
    db.controls["o"] = vh_down
    db.controls["l"] = vl_up
    db.controls["."] = vl_down
    
    # Set range for green color and 
    # define mask
    color_lower = np.array([110,50,50], np.uint8) #(255, 255, 130) #BGR
    color_upper = np.array([130,255,255], np.uint8) #(131, 67, 18)  #BGR
    kernel = np.ones((5, 5), "uint8")

    loop_count = 0
    # The start of this loop should be exactly as it's shown below. Any changes and it might not work
    # as expected. Use the CV image however you want to analyze drone video and call drone functions 
    # to move drone as desired.
    while exiting.get() == False: # Loop until exiting is signaled
        db.process_keyboard()  # Process keystrokes
        lcurrent_frame = current_frame.get() # Get video frame
        if lcurrent_frame != None:
            image = db.process_frame(lcurrent_frame) # Process
            # Change nothing above here!  Use image however you 
            # want to analyze drone position, movement, etc.
            # image is a CV2 image.

            # Here is an example to show a secondary CV2
            # window.  loop_count keeps it updating only
            # once per 30 frames (which is a good idea
            # for efficiency sake.)
            loop_count += 1
            if loop_count % 5 == 0:

                # Analyze video cv2 color detection
#                hsvFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#                green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
#                green_mask = cv2.dilate(green_mask, kernal)
#                res_green = cv2.bitwise_and(image, image,
#                                            mask = green_mask)

#                blurred = cv2.GaussianBlur(image, (11, 11), 0)

                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                lower_hsv = np.array([ilowH, ilowS, ilowV])
                higher_hsv = np.array([ihighH, ihighS, ihighV])
                # Apply the cv2.inrange method to create a mask
                mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
                # Apply the mask on the image to extract the original color
                frame = cv2.bitwise_and(image, image, mask=mask)


#                mask = cv2.erode(mask, None, iterations=2)
#                mask = cv2.dilate(mask, None, iterations=2)

#                res = cv2.bitwise_and(image, image, mask = mask)

                # Convert to BGR Gray
#                mask2 = cv2.cvtColor(hsv.copy(), cv2.COLOR_BGR2GRAY)

                # reduce the noise
                opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#                contours = imutils.grab_contours(contours)
#                contours = contours[0]
                # Get dimensions of everything
#                x = 10000
#                y = 10000
#                w = 0
#                y = 0

#                for contour in contours:
#                    x,y,w,h = cv2.boundingRect(contour)
#                    if w>5 and h>10:
#                    cv2.rectangle(image,(x,y),(x+w,y+h),(155,155,0),1)

                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)

                    extLeft = tuple(c[c[:, :, 0].argmin()][0])
                    extRight = tuple(c[c[:, :, 0].argmax()][0])
                    extTop = tuple(c[c[:, :, 1].argmin()][0])
                    extBot = tuple(c[c[:, :, 1].argmax()][0])

                    cv2.rectangle(frame, extTop, extBot, (0, 255, 0), 3)

                cv2.putText(frame, str(ihighH), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, str(ilowH), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, str(ihighS), (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, str(ilowS), (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, str(ihighV), (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(frame, str(ilowV), (300, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # CV way of showing video
                cv2.imshow('Secondary View', frame)
                _ = cv2.waitKey(1) & 0xFF

def hh_up(drone, speed):
    global ihighH
    if ihighH < 180:
        ihighH += 1

def hh_down(drone, speed):
    global ihighH
    if ihighH > -1:
        ihighH -= 1

def hl_up(drone, speed):
    global ilowH
    if ilowH < 180:
        ilowH += 1

def hl_down(drone, speed):
    global ilowH
    if ilowH > -1:
        ilowH -= 1

def sh_up(drone, speed):
    global ihighS
    if ihighS < 255:
        ihighS += 1

def sh_down(drone, speed):
    global ihighS
    if ihighS > -1:
        ihighS -= 1

def sl_up(drone, speed):
    global ilowS
    if ilowS < 255:
        ilowS += 1

def sl_down(drone, speed):
    global ilowS
    if ilowS > -1:
        ilowS -= 1

def vh_up(drone, speed):
    global ihighV
    if ihighV < 255:
        ihighV += 1

def vh_down(drone, speed):
    global ihighV
    if ihighV > -1:
        ihighV -= 1

def vl_up(drone, speed):
    global ilowV
    if ilowV < 255:
        ilowV += 1

def vl_down(drone, speed):
    global ilowV
    if ilowV > -1:
        ilowV -= 1

if __name__ == '__main__':
    main()
