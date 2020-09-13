import os
import sys
from datetime import datetime
from makebinary import makebinary

# enable switching to picamera from commandline call (pass in 'picamera')
if len(sys.argv) == 1:
    capture_method = 'gphoto'
else:
    capture_method = sys.argv[1]

basedir = '/home/pi/Pictures'
# The radius in pixels of the fisheye lens area, set to None if no fisheye lens
fisheye_radius = 1000

# capture an image with the specified method
if capture_method.lower() == 'gphoto':
    import subprocess
    out = subprocess.check_output(['gphoto2', '--capture-image-and-download'])
    for line in out.split('\n'):
        if 'Saving file as' in line:
            file = line.split(' ')[3]
            break
    else:
        raise Exception('GPhoto image capture and save unsuccessful.')
elif capture_method.lower() == 'picamera':
    from picamera import PiCamera
    from time import sleep

    # open the camera and take the latest image
    file = 'latest.jpg'
    camera = PiCamera()
    camera.start_preview()
    sleep(2)             # wait for the camera to initialise
    camera.capture(file) # capture and save an image to 'file'
else:
    raise Exception("Invalid capture method {}. Use 'gphoto' or 'picamera'."
                    .format(capture_method))

# capture the timestamp
now = datetime.now()
# create the relevant folders if they don't already exist
os.makedirs(basedir + now.strftime("%Y/%m/%d"), exist_ok=True)

# move the new image to within its relevant folder with a timestamped filename
new_file = basedir + now.strftime("%Y/%m/%d/%Y-%m-%d-%H-%M-%S.jpg")
os.rename(file, new_file)

# process as desired (compute cloud coverage and mask image)
makebinary(new_file, fisheye_radius)
