'''
DBQueue - Demonstrates queuing items for
the drone to process.  Press 'C' to start/stop
processing items in the queue.

(c)2022. Brett Huffman
v.02
---------------------------------------
'''
from libs.DroneBLib import DroneB, Queue_Item
from libs.DroneBLib import exiting, current_frame
import cv2

def main():
    db = DroneB()
    db.start(custom_loop = True)


    # Fill command queue with items to process
    db.AddNewQueueItem("takeoff", 2000)
    for i in range(12):
        db.AddNewQueueItem("yaw_left", 500)
        db.AddNewQueueItem("right", 500)
        db.AddNewQueueItem("forward", 300)
    db.AddNewQueueItem("land", 1000)



    # The start of this loop should be exactly as it's shown below. Any changes and it might not work
    # as expected. Use the CV image however you want to analyze drone video and call drone functions 
    # to move drone as desired.
    while exiting.get() == False: # Loop until exiting is signaled
        db.process_keyboard()  # Process keystrokes
        lcurrent_frame = current_frame.get() # Get video frame
        if lcurrent_frame != None:
            image = db.process_frame(lcurrent_frame) # Process

        # Once the command queue is enabled, process them
        # one-by-one until it's empty
        db.process_command_queue() # Process the command queue

if __name__ == '__main__':
    main()