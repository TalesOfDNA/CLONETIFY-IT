import skimage
from skimage.io import imread, imsave
import numpy as np
from skimage.color import rgb2gray
from skimage import io as skio
import cv2


img = skio.imread("SEGMENTED.png")
#img = rgb2gray(img)
print("dtype of image: {}".format(img.dtype))

from skimage import filters
sobel = filters.sobel(img)

import matplotlib.pyplot as plt

plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['figure.dpi'] = 200

plt.imshow(sobel)
plt.show()

blurred = filters.gaussian(sobel, sigma=2.0)
plt.imshow(blurred)
plt.show()

cv2.imwrite('sobel.png', blurred)

light_spots = np.array((img > 200).nonzero()).T
plt.plot(light_spots[:, 1], light_spots[:, 0], 'o')
plt.imshow(img)
plt.title('light spots in image')
plt.show()


dark_spots = np.array((img < 3).nonzero()).T

plt.plot(dark_spots[:, 1], dark_spots[:, 0], 'o')
plt.imshow(img)
plt.title('dark spots in image')
plt.show()

from scipy import ndimage as ndi
bool_mask = np.zeros(img.shape, dtype=np.bool)
bool_mask[tuple(light_spots.T)] = True
bool_mask[tuple(dark_spots.T)] = True
seed_mask, num_seeds = ndi.label(bool_mask)
num_seeds

from skimage import morphology
ws = morphology.watershed(blurred, seed_mask)
plt.imshow(ws)
plt.show()

cv2.waitKey(0)
