

from scipy import ndimage as ndi
import matplotlib.pyplot as plt
import skimage
from skimage.morphology import watershed, disk
from skimage import data
from skimage.filters import rank
from skimage.util import img_as_ubyte
from skimage import io
from skimage.color import rgb2gray
from skimage.io import imsave
from skimage import filters


image = io.imread('Frame_brighter2.png')
image = rgb2gray(image)

# denoise image
denoised = rank.median(image, disk(2))

# find continuous region (low gradient -
# where less than 10 for this image) --> markers
# disk(5) is used here to get a more smooth image
markers = rank.gradient(denoised, disk(5)) < 10
markers = ndi.label(markers)[0]

# local gradient (disk(2) is used to keep edges thin)
gradient = rank.gradient(denoised, disk(3))

skimage.io.imsave('New.png', gradient)

img = io.imread('New.png')

blurred = filters.gaussian(img, sigma=2.0)
import numpy as np
light_spots = np.array((img > 245).nonzero()).T
dark_spots = np.array((img < 3).nonzero()).T

from scipy import ndimage as ndi
bool_mask = np.zeros(img.shape, dtype=np.bool)
bool_mask[tuple(light_spots.T)] = True
bool_mask[tuple(dark_spots.T)] = True
seed_mask, num_seeds = ndi.label(bool_mask)
print(num_seeds)

from skimage import morphology
ws = morphology.watershed(blurred, seed_mask)
#plt.imshow(ws)


# display results
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8),
                         sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax[0].set_title("Original")

ax[1].imshow(gradient, cmap=plt.cm.nipy_spectral, interpolation='nearest')
ax[1].set_title("Local Gradient")

ax[2].imshow(ws, cmap=plt.cm.gray, interpolation='nearest')
ax[2].set_title("Last One")

ax[3].imshow(gradient, cmap=plt.cm.gray, interpolation='nearest')
ax[3].set_title("Back to Gray")


for a in ax:
    a.axis('off')

fig.tight_layout()
plt.show()