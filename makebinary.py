# Cloud coverage computation for on-board computation
import os
import cv2
import numpy as np
from datetime import datetime

def preprocess(image):
    """ Preprocess 'image' to help separate cloud and sky. """
    B, G, R = cv2.split(image) # extract the colour channels

    # construct a ratio between the blue and red channel sum and difference
    BR_sum  = B + R
    BR_diff = B - R
    # handle X/0 and 0/0 errors, and remove NaNs (not a number)
    with np.errstate(divide='ignore', invalid='ignore'):
        BR_ratio = BR_diff / BR_sum
        BR_ratio = np.nan_to_num(BR_ratio)

    # normalize to 0-255 range and convert to 8-bit unsigned integers
    return cv2.normalize(BR_ratio, None, 0, 255, cv2.NORM_MINMAX) \
              .astype(np.uint8)

def makebinary(imagepath, radiusMask = None):
    startTime = datetime.now()

    # read in the image and shrink for faster processing
    image   = cv2.imread(imagepath)
    scale   = 0.2
    smaller = cv2.resize(image, (0,0), fx=scale, fy=scale)
    center  = [dim / 2 for dim in smaller.shape[:2]]

    preprocessed = preprocess(smaller.astype(float))

    if radiusMask:
        # apply a circular mask to get only the pixels of interest
        from cmask import cmask
        mask   = cmask(index, resize_factor * radiusMask, resized).astype(bool)
    else:
        mask   = np.ones(preprocessed.shape).astype(bool)
    
    masked = preprocessed[mask]

    # use Otsu's method to separate clouds and sky
    threshold, result = cv2.threshold(masked, 0, 255,
                                      cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # invert the result so clouds are white (255) and sky is black (0)
    inverted = cv2.bitwise_not(result)

    # determine the cloud coverage
    cloud_pixels   = np.count_nonzero(inverted == 255)
    total_pixels   = result.size
    cloud_coverage = cloud_pixels / total_pixels

    # create a mask of where the clouds are
    cloud_image_mask = np.zeros(mask.shape, dtype=np.uint8)
    cloud_image_mask[mask] = inverted.flatten()

    print('Coverage is {:.3f}%'.format(cloud_coverage*100))
    print(datetime.now() - startTime)

    last_dot  = imagepath.rindex('.')
    save_path = imagepath[:last_dot] + '-mask' + imagepath[last_dot:]
    cv2.imwrite(save_path, cloud_image_mask)

    return(cloud_coverage)
