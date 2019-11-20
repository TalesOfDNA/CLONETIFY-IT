# from math import sqrt
# from skimage import data
# from skimage.feature import blob_dog, blob_log, blob_doh
# from skimage.color import rgb2gray
# from skimage import io
# import matplotlib.pyplot as plt


# image = io.imread('Frame2.jpg')[0:500, 0:500]
# image_gray = rgb2gray(image)

# blobs_log = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)

# # Compute radii in the 3rd column.
# blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

# blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
# blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

# blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)

# blobs_list = [blobs_log, blobs_dog, blobs_doh]
# colors = ['yellow', 'lime', 'red']
# titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
#           'Determinant of Hessian']
# sequence = zip(blobs_list, colors, titles)

# fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True)
# ax = axes.ravel()

# for idx, (blobs, color, title) in enumerate(sequence):
#     ax[idx].set_title(title)
#     ax[idx].imshow(image, interpolation='nearest')
#     for blob in blobs:
#         y, x, r = blob
#         c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
#         ax[idx].add_patch(c)
#     ax[idx].set_axis_off()

# plt.tight_layout()
# plt.show()



from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color 
from skimage import filters 
from scipy import ndimage

from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage.measure import regionprops, label

image = color.rgb2gray(io.imread('Frame2.jpg', plugin='freeimage'))
image = image < filters.threshold_otsu(image)

distance = ndimage.distance_transform_edt(image)

# Here's one way to measure the number of coins directly
# from the distance map
coin_centres = (distance > 0.8 * distance.max())
print('Number of coins (method 1):', np.max(label(coin_centres)))

# Or you can proceed with the watershed labeling
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
                            labels=image)


markers, num_features = ndimage.label(local_maxi)
labels = watershed(-distance, markers, mask=image)

# ...but then you have to clean up the tiny intersections between coins
regions = regionprops(labels)
regions = [r for r in regions if r.area > 50]

print('Number of coins (method 2):', len(regions) - 1)

fig, axes = plt.subplots(ncols=3, figsize=(8, 2.7))
ax0, ax1, ax2 = axes

ax0.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
ax0.set_title('Overlapping objects')
ax1.imshow(-distance, cmap=plt.cm.jet, interpolation='nearest')
ax1.set_title('Distances')
ax2.imshow(labels, cmap=plt.cm.spectral, interpolation='nearest')
ax2.set_title('Separated objects')

for ax in axes:
    ax.axis('off')

fig.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                    right=1)
plt.show()