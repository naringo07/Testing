'''
DBQR.py - reads qr codes and prints to the
text to the screen

(c)2022. Brett Huffman
v.02
---------------------------------------
'''
from libs.DroneBLib import DroneB
from libs.DroneBLib import exiting, current_frame
import cv2
from libs.QR import read_qr_code

def main():
    db = DroneB()
    db.start(custom_loop = True)

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
            if loop_count % 30 == 0:
                # Look for QR - if read put text on screen
                val = read_qr_code(image=image)


                cv2.putText(image, val[0], (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                cv2.rectangle(image, val[0][0], val[0][4], (0, 255, 0), 3)
                # CV way of showing video
                cv2.imshow('Secondary View', image)
                _ = cv2.waitKey(1) & 0xFF

if __name__ == '__main__':
    main()