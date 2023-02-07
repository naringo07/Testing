# DroneB
#### ©2022. Brett Huffman
#### v.02
---------------------------------------

The DroneB project is meant to act as a starting point for Tello Drone programming in the Intro to Programming course at Principia College.

## Files Included
There are several python files available for use:

- DroneBLib.py - A library module that can be included in your python project to expose the DroneB functionality to your own program.  This includes to sample files:

    - BasicB.py - Shows how to use the DroneBlib.py in a minimalistic way.

    - AdvB.py - a more advanced way to use DroneBlib.py.  Be sure to read the comments in the AdvB.py file to see how to use it.

    - DBQR.py - another advanced pythong script that displays the text of a QR code when read.

- QR.py - a library to read QR files

## Installation
To use this library, you must include the following with the pip3 command:

- opencv-python
- tellopy
- av
- numpy
- pygame
- image

Install these libraries with the command:

    pip3 install <library>

ie:

    pip3 install opencv-python

## Execution Demo Programs
Execute the programs with the following:

    python <script>

ie

    python ./BasicB.py

## Using Libraries Yourself
Place the DroneBLib.py file into your project and include the module in 
your python script.  Finally, create a DroneB object 
to control the drone:

    from DroneBLib import DroneB

    def main():
        db = DroneB()
        db.start()

    if __name__ == '__main__':
        main()

## Drone Controls
Out of the box, the following key controls are available for operating the drone.

Tab - lift off
WASD - Drone Forward, Left, Right, Back
Q/E - slow yaw
Arrow keys - ascend, descend, or yaw
H - toggle HUD
Backspace - land
P - palm-land
Enter - take picture
R - toggle recording
C - toggle command queue on/off
X - toggle forward / downward cam (Only on edu model drone)

## Credits
Credit goes to the excellent work done by the following individuals/groups:
- Hanyazou for many of the ideas in these modules: https://github.com/hanyazou/TelloPy
- Hacking Drones by GoBot: https://gobot.io/blog/2018/04/20/hello-tello-hacking-drones-with-go/
- Kragrathea's C# Tello project: https://github.com/Kragrathea/TelloLib

---
MIT License

Copyright (c) 2022 Brett Huffman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.