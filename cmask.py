# This function generates the circular mask for the input fish-eye image

# Input:
# index = center co-ordanates of the image
# radius = radius of the circular image
# array = input image

# Output:
# image_mask = binary output image

import numpy as np

def cmask(index,radius,array):
  	
  a,b = index
  is_rgb = len(array.shape)

  if is_rgb == 3:
     ash = array.shape
     nx=ash[0]
     ny=ash[1]

  else:
     nx,ny = array.shape
  
  s = (nx,ny)
  image_mask = np.zeros(s)
  y,x = np.ogrid[-a:nx-a,-b:ny-b]
  mask = x*x + y*y <= radius*radius
  image_mask[mask] = 1
  return(image_mask)
