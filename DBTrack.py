'''
DBTrack.py - Track blue squares with queues.  Once
user presses 'C', the drone will automatically
track a blue square (use blue tape on the wall to demo).

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
ihighS = 200
ilowS = 94
ihighV = 130
ilowV = 30

def main():


    db = DroneB()
    db.start(custom_loop = True)
    
    # Set range for green color and 
    # define mask
    higher_hsv = np.array([180,255,130], np.uint8) #(131, 67, 18)  #BGR
    lower_hsv = np.array([52,94,30], np.uint8) #(255, 255, 130) #BGR
    kernel = np.ones((5, 5), "uint8")

    loop_count = 0
    # The start of this loop should be exactly as it's shown below. Any changes and it might not work
    # as expected. Use the CV image however you want to analyze drone video and call drone functions 
    # to move drone as desired.
    while exiting.get() == False: # Loop until exiting is signaled
        db.process_keyboard()  # Process keystrokes
        # Once the command queue is enabled, process them
        # one-by-one until it's empty
        db.process_command_queue() # Process the command queue
        lcurrent_frame = current_frame.get() # Get video frame
        if lcurrent_frame != None:
            image = db.process_frame(lcurrent_frame) # Process
            # Change nothing above here!  Use image however you 
            # want to analyze drone position, movement, etc.
            # image is a CV2 image.

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
                mask2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                contours, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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

                extLeft = None
                extRight = None
                extTop = None
                extBot = None
                
                if len(contours) > 0:
                    c = max(contours, key=cv2.contourArea)

                    extLeft = tuple(c[c[:, :, 0].argmin()][0])
                    extRight = tuple(c[c[:, :, 0].argmax()][0])
                    extTop = tuple(c[c[:, :, 1].argmin()][0])
                    extBot = tuple(c[c[:, :, 1].argmax()][0])

                    cv2.rectangle(frame, extTop, extBot, (0, 255, 0), 3)
                else:
                    continue

#                cv2.putText(frame, str(ihighH), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
#                cv2.putText(frame, str(ilowH), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                ''' Determine how much to move
                The axes are shown below (assuming a frame width and height of 600x400):
                +Y                 (0,200)

                Y  (-300, 0)        (0,0)               (300,0)

                -Y                 (0,-200)
                -X                    X                    +X
                '''
                if  abs(extBot[0] - extTop[0]) > 40 and abs(extBot[1] - extTop[1]) > 40:
                    # Get image midpoint and calculate diff
                    height, width, channels = frame.shape
                    image_mid = (width // 2, height // 2)
                    obj_mid = (extTop[0] + (extBot[0] - extTop[0])//2, extTop[1] + (extBot[1] - extTop[1])//2)

                    # Draw them on the image
                    cv2.circle(frame, image_mid, 4, (255, 255, 255))
                    cv2.circle(frame, obj_mid, 4, (255, 0, 255))

                    # Do a little proportion here
                    # 40 pixels   =   diff
                    #  3 seconds      X
                    prop_x_to_move = int(10 * (image_mid[0] - obj_mid[0])//40)
                    prop_y_to_move = int(10 * (image_mid[1] - obj_mid[1])//40)

                    if db.command_queue_active == True and db.command_queue_enable == True:
                        if prop_x_to_move > 5:
                            print("Sent left", abs(prop_x_to_move))
                            db.AddNewQueueItem("left", abs(prop_x_to_move))
                        elif prop_x_to_move < -5:
                            print("Sent right", abs(prop_x_to_move))
                            db.AddNewQueueItem("right", abs(prop_x_to_move))

                        if prop_y_to_move > 5:
                            print("Sent up", abs(prop_x_to_move))
                            db.AddNewQueueItem("up", abs(prop_x_to_move))
                        elif prop_y_to_move < -5:
                            print("Sent down", abs(prop_x_to_move))
                            db.AddNewQueueItem("down", abs(prop_x_to_move))

                # CV way of showing video
                cv2.imshow('Secondary View', frame)
                _ = cv2.waitKey(1) & 0xFF


if __name__ == '__main__':
    main()
