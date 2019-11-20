import skimage
skimage.__version__

import numpy as np
import matplotlib.pyplot  as plt
import cv2
from skimage import filters
from skimage import feature
from skimage.io import imread, imsave
from skimage.color import rgb2gray

image = imread("cells1.png")
image_gray = rgb2gray(image)
from skimage import filters
sobel = filters.sobel(image_gray)
#image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_denoised = filters.median(sobel, selem=np.ones((5,5)))

plt.plot(image_denoised)
plt.show()

from skimage import img_as_uint
#edges = img_as_uint(skimage.feature.canny(image_gray, sigma=2))
edges = skimage.feature.canny(image_gray, sigma=2)

from scipy.ndimage import distance_transform_edt
dt = distance_transform_edt(~edges)

#local_max = img_as_uint(feature.peak_local_max(dt, indices=False, min_distance=5))

local_max = feature.peak_local_max(dt, indices=False, min_distance=5)
peak_idx = feature.peak_local_max(dt, indices=True, min_distance=5)
print(peak_idx[:10])
plt.plot(peak_idx[:,1], peak_idx[:,0], 'r.')
plt.imshow(dt)
plt.show()

from skimage import measure
markers = measure.label(local_max)

from skimage import morphology, segmentation

labels = morphology.watershed(-dt, markers)
plt.imshow(segmentation.mark_boundaries(image_gray, labels))
plt.show()

from skimage import color
plt.imshow(color.label2rgb(labels, image=image_gray))
plt.show()


plt.imshow(color.label2rgb(labels, image=image_gray, kind='avg'), cmap='gray')
plt.show()

regions = measure.regionprops(labels, intensity_image = image_gray)
region_means = [r.mean_intensity for r in regions]
plt.hist(region_means, bins=20)
plt.show()

from sklearn.cluster import KMeans
model = KMeans(n_clusters=2)

region_means = np.array(region_means).reshape(-1, 1)
model.fit(np.array(region_means).reshape(-1, 1))
print(model.cluster_centers_)

bg_fg_labels = model.predict(region_means)
bg_fg_labels

classified_labels = labels.copy()
for bg_fg, region in zip(bg_fg_labels, regions):
    classified_labels[tuple(region.coords.T)] = bg_fg


plt.imshow(color.label2rgb(classified_labels, image=image_gray))
plt.show()

print(classified_labels)

from skimage.color import rgb2gray
from skimage.io import imread, imsave
from skimage.filters import threshold_otsu
from skimage import img_as_uint

pre_processed = (color.label2rgb(labels, image=image, kind='avg'))
imsave("SEGMENTED1.png", img_as_uint(pre_processed))
#img_gray = rgb2gray(pre_processed)
#pre_processed = color.label2rgb(classified_labels, image=image_gray)
#pre_processed1 = img_as_uint(pre_processed)
#ret, image_edged = cv2.threshold(pre_processed1, 90, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#binary_thresh_img = img_gray; thresh

plt.imshow(pre_processed)
plt.show()

#cv2.imshow("Original", image)
# cv2.imshow("denoised", image_denoised)
# cv2.imshow("edge", edges)
# #cv2.imshow("dt", dt)
# cv2.imshow("max", local_max)



cv2.waitKey(0)
