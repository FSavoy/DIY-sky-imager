import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from collections import namedtuple
from showasImage import *
from normalize_array import *
import colorsys


def color16mask(input_image,mask_image):
	# All matrices are normalized from 0 to 1
	mask_image = mask_image.astype(float)
	
	
	[rows,cols]=mask_image.shape
	
	# Input image is a numpy 3D array
	ColorChannel = namedtuple("ColorChannel", "c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 c16")
	
	red = input_image[:,:,2]
	green = input_image[:,:,1]
	blue = input_image[:,:,0]
	
	red = red.astype(float)
	green = green.astype(float)
	blue = blue.astype(float)
	
	# RGB images for transfer
	red_image = np.multiply(red,mask_image)
	green_image = np.multiply(green,mask_image)
	blue_image = np.multiply(blue,mask_image)
	
	
	
	im_mask = mask_image.flatten()
	find_loc = np.where(im_mask==1)
	find_loc = list(find_loc)
	
	red = red.flatten()
	blue = blue.flatten()
	green = green.flatten()

	red_select = red[list(find_loc)]
	green_select = green[list(find_loc)]
	blue_select = blue[list(find_loc)]
	
	
	# HSV image
	H_select = []
	S_select = []
	V_select = []
	for _,index in enumerate(red_select):

		r_value =  red_select[index]
		g_value = green_select[index]
		b_value = blue_select[index]
		
		hsv_tuple = colorsys.rgb_to_hsv(r_value,g_value,b_value)
		H_select.append(hsv_tuple[0])
		S_select.append(hsv_tuple[1])
		V_select.append(hsv_tuple[2])
	
	H_select = np.asarray(H_select)
	S_select = np.asarray(S_select)
	V_select = np.asarray(V_select)
	H = showasImage(H_select)
	S = showasImage(S_select)
	V = showasImage(V_select)
	

	# BR image
	br_num = blue_select - red_select
	br_den = blue_select + red_select
	BR = br_num/br_den
	BR[np.isnan(BR)] = 0  # Replacing all NANs with 0
	BR = showasImage(BR)  # Scale it to 0 to 255.


	# Final image (with proper mask) for transfer
	index = 0
	BR_image = np.zeros([rows,cols])
	H_image = np.zeros([rows,cols])
	S_image = np.zeros([rows,cols])
	V_image = np.zeros([rows,cols])
	
	
	for i in range(0,rows):
		for j in range(0,cols):

			if mask_image[i,j]==1:
				
				BR_image[i,j] = BR[index]
				
				H_image[i,j] = H[index]
				S_image[i,j] = S[index]
				V_image[i,j] = V[index]
				
				index = index + 1
			
	
	cc = ColorChannel(c1 = red_image, c2 = green_image, c3 = blue_image ,c4 = H_image, c5 = S_image, c6 = V_image,c7 = "foo", c8 = "bar", c9 = "baz",c10 = "foo", c11 = "bar", c12 = "baz",c13 = "foo",c14 = "foo", c15 = BR_image, c16 = "baz")
	# Please note that all color channels are not computed here. We put some dummy characters in a few of them.

	return(cc)
