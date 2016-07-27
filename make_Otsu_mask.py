# This function computes the clustering on c15 color channel.
# Input:
# input_matrix = input image
# mask_image = mask image

# Output:
# Th_image: Binary output image
# cloud_coverage : Cloud coverage ratio (the value lies between 0 and 1)

import numpy as np
import cv2
#from sklearn.cluster import KMeans


def make_Otsu_mask(input_matrix,mask_image):
	
	[rows,cols]=mask_image.shape
	
	im_mask_flt = mask_image.flatten()
	find_loc = np.where(im_mask_flt==1)
	find_loc = list(find_loc)
	
	input_vector = input_matrix.flatten()
	
	input_select = input_vector[list(find_loc)]
	
	
	X = input_select.reshape(-1, 1)
	
	ratio_image  = np.array(X, np.uint8)
	ret,thresh1 = cv2.threshold(ratio_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	#print (ret)
	


	
	
	# 0 is sky and 1 is cloud
	cloud_pixels = np.count_nonzero(thresh1 == 0)
	sky_pixels = np.count_nonzero(thresh1 == 255)
	total_pixels = cloud_pixels + sky_pixels
	
	#print (cloud_pixels,total_pixels)
	cloud_coverage = float(cloud_pixels)/float(total_pixels)
	
	# Final threshold image for transfer
	
	thresh1 = 255 - thresh1
	index = 0
	Th_image = np.zeros([rows,cols])
	for i in range(0,rows):
		for j in range(0,cols):
			
			if mask_image[i,j]==1:
				#print (i,j)
				#print (index)
				Th_image[i,j] = thresh1[index]
				index = index + 1
			

	return(Th_image,cloud_coverage)
