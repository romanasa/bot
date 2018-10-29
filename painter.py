from sklearn.cluster import KMeans
from skimage.io import imread
from skimage import img_as_float
import numpy as np
import pylab


class Painter:
	def __init__(self, path):
		self.path = path

	def paint(self, cnt):
		image = imread(self.path)
		data = img_as_float(image)

		X = []
		for row in data:
			for pixel in row:
				X.append(pixel)

		n = len(data)
		m = len(data[0])

		clf = KMeans(n_clusters=cnt, init='k-means++', n_init=2, random_state=241, max_iter=30)
		clf.fit(X)

		classesR = [[] for i in range(cnt)]
		classesG = [[] for i in range(cnt)]
		classesB = [[] for i in range(cnt)]

		for i in range(len(X)):
			classesR[clf.labels_[i]].append(X[i][0])
			classesG[clf.labels_[i]].append(X[i][1])
			classesB[clf.labels_[i]].append(X[i][2])

		mean = [(0, 0, 0)] * cnt

		for color in range(cnt):
			t = np.mean(classesR[color])
			mean[color] = (np.mean(classesR[color]), np.mean(classesG[color]), np.mean(classesB[color]))

		xMean = X[::]

		for i in range(len(X)):
			xMean[i] = mean[clf.labels_[i]]

		image_mean = np.reshape(xMean, (n, m, 3))
		pylab.imsave('modif' + self.path, image_mean)


    # pylab.imshow(np.reshape(xMean, (n, m, 3)))
    # pylab.show()
