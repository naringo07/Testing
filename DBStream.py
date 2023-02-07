'''
AdvB - The more complicated example of using
the Tello Drone Starter Library.  You must 
specify custom_loop = True in the start()
command.  Next, make sure to then loop which
handles keystrokes, displaying video and
sending commands to the drone.

(c)2022. Brett Huffman
v.02
---------------------------------------
'''
from libs.DroneBLib import DroneB
from libs.DroneBLib import exiting, current_frame
import cv2
import subprocess as sp

def main():
    db = DroneB()
    db.start(custom_loop = True)

    # Setup streaming

    height, width, ch = lcurrent_frame.shape
    height, width = 480, 600

    ffmpeg = 'FFMPEG'
    dimension = '{}x{}'.format(width, height)
    f_format = 'bgr24' # remember OpenCV uses bgr format

    command = [ffmpeg,
            '-y',
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-s', dimension,
            '-pix_fmt', 'bgr24',
            '-i', '-',
            '-an',
            '-v', '0',
            '-vcodec', 'mpeg4',
            '-b:v', '5000k',
            '=f', 'mpegts', 'udp://127.0.0.1:23000']

    proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

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

            proc.stdin.write(image.tostring())

    # Close down stdin and stderr
    proc.stdin.close()
    proc.stderr.close()
    proc.wait()


            '''
            # Use a combination of these...
            (Stream like this)
            $ ffmpeg -i sample.mp4 -v 0 -vcodec mpeg4 -f mpegts udp://127.0.0.1:23000

            # This script copies the video frame by frame
            import cv2
            import subprocess as sp

            input_file = 'input_file_name.mp4'
            output_file = 'output_file_name.mp4'

            cap = cv2.VideoCapture(input_file)
            ret, frame = cap.read()
            height, width, ch = frame.shape

            ffmpeg = 'FFMPEG'
            dimension = '{}x{}'.format(width, height)
            f_format = 'bgr24' # remember OpenCV uses bgr format
            fps = str(cap.get(cv2.CAP_PROP_FPS))

            command = [ffmpeg,
                    '-y',
                    '-f', 'rawvideo',
                    '-vcodec','rawvideo',
                    '-s', dimension,
                    '-pix_fmt', 'bgr24',
                    '-r', fps,
                    '-i', '-',
                    '-an',
                    '-vcodec', 'mpeg4',
                    '-b:v', '5000k',
                    output_file ]

            proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                proc.stdin.write(frame.tostring())

            cap.release()
            proc.stdin.close()
            proc.stderr.close()
            proc.wait()



            Can check this with ffplay like this:
            ffplay udp://127.0.0.1:23000
            '''

if __name__ == '__main__':
    main()