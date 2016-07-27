# Cloud coverage computation for on-board computation
import cv2
import numpy as np
import os
from datetime import datetime

# User defined functions
from normalize_array import *
from cmask import *
from color16mask import *
from make_Otsu_mask import *


def makebinary(imagepath, radiusMask = None):
	startTime = datetime.now()

	# Read the input image. Mention the complete path of the image
	#imagepath = './corrWahrsis3.jpg'
	im = cv2.imread(imagepath)


	# ---------- Resized -------------
	# Resize the image for speeding purposes
	resize_factor = 0.2
	im_re = cv2.resize(im, (0,0), fx=resize_factor, fy=resize_factor)
	index = [np.shape(im_re)[0]/2, np.shape(im_re)[1]/2]#[345, 518]  # Center of the image
	if radiusMask:
		im_mask = cmask(index,resize_factor*radiusMask,im_re) # Mask with radius 200 pixels
	else:
		s = (np.shape(im_re)[0],np.shape(im_re)[1])
		im_mask = np.ones(s)
	# Extract the color channels
	(cc) = color16mask(im_re,im_mask)


	# Performing clustering on the c15 color channel
	inp_mat = cc.c15


	#(th_img,coverage) = make_cluster_mask(inp_mat,im_mask)
	(th_img,coverage) = make_Otsu_mask(inp_mat,im_mask)

	print ('Coverage is ',coverage)

	print (datetime.now() - startTime)
	
	
	path_components = imagepath.split("/")
	full_image_name = path_components[-1]
	imagenameparts = full_image_name.split(".")
	image_name = imagenameparts[0]
	ext_name = imagenameparts[1]

	save_path = '/'.join(path_components[:-1]) + '/' + image_name + '-mask.' + ext_name	

	cv2.imwrite(save_path,th_img)

	return(coverage)

