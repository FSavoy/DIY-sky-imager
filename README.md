# A tutorial to build your own Sky Imager with cloud coverage estimation

In this tutorial, you learn how to create your own custom made Sky Imager. You program a Raspberry Pi to instruct a camera to take pictures of the sky at regular intervals. You install a web interface to access the captured images and you apply signal processing techniques to compute the cloud coverage.

The main file is tutorial.pdf. This repository contains all the scripts required for the project.

This project is a join work from:
- Soumyabrata Dev, Nanyang Technological University, Singapore
- Florian M. Savoy, Advanced Digital Sciences Center, University of Illinois at Urbana-Champain, Singapore
- Yee Hui Lee, Nanyang Technological University, Singapore
- Stefan Winkler, Advanced Digital Sciences Center, University of Illinois at Urbana-Champain, Singapore

-----
Modified to be more efficient, understandable, and pythonic by ES-Alexander.

Can be switched to using the PiCamera library by adding 'picamera' to the end of the `chrontab` modification in the tutorial.  
`*/2 7-19 * * * python /home/pi/DIY-sky-imager/capture_image.py`  
-> `*/2 7-19 * * * python /home/pi/DIY-sky-imager/capture_image.py picamera`
