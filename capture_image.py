import subprocess
import datetime
import os


basedir = '/home/pi/Pictures'
fisheye_radius = 1000 # The radius in pixels of the fisheye lens area, set to None if no fisheye lens


out = subprocess.check_output(['gphoto2', '--capture-image-and-download'])

file = []
for outline in out.split("\n"):
        if "Saving file as" in outline:
                file.append(outline.split(' ')[3])

if file:
	now = datetime.datetime.now()
	if not os.path.isdir(basedir + now.strftime("%Y")):
		os.mkdir(basedir + now.strftime("%Y"))
	if not os.path.isdir(basedir + now.strftime("%Y/%m")):
		os.mkdir(basedir + now.strftime("%Y/%m"))
	if not os.path.isdir(basedir + now.strftime("%Y/%m/%d")):
		os.mkdir(basedir + now.strftime("%Y/%m/%d"))

	os.rename(file[0], basedir + now.strftime("%Y/%m/%d/%Y-%m-%d-%H-%M-%S.jpg"))

	# Only imported if needed
	from makebinary import *
	makebinary(file[0], fisheye_radius)
