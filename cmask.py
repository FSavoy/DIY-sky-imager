# This function generates the circular mask for the input fish-eye image

# Input:
# center = center co-ordanates of the image (row, col)
# radius = radius of the circular image
# array  = input image

# Output:
# image_mask = binary output image

import numpy as np

def cmask(center, radius, image):
  c_y, c_x = center
  num_y, num_x = image.shape[:2]

  image_mask = np.ones((num_y, num_x))
  y, x = np.ogrid[-c_y:num_y-c_y, -c_x:num_x-c_x]
  # remove components outside the circle
  image_mask[(x*x + y*y) > radius*radius] = 0
  return(image_mask)
