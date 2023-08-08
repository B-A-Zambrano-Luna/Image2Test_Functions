# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:15:27 2022

@author: LENOVO
"""
import skimage.io
from matplotlib import pyplot as plt
import Q_p
import numpy as np
import image2test
from Q_p_as_fractal import Christiakov_emmending
import time
from keras.datasets import mnist
from skimage.transform import resize

(train_X, train_y), (test_X, test_y) = mnist.load_data()

# imgs = train_X[:5000]
p = 3
k = 6
Z_k = Q_p.Z_N_group(p, k)
image = resize(train_X[0], (27, 27))
image = 1*(image > 0.3)

image_1 = np.array([[11, 12, 13],
                    [21, 22, 23],
                    [31, 32, 33]])
inicio = time.time()
image_12test = image2test.imate2test(image, Z_k,
                                     reduction=False)
image_12test.fit()
values = image_12test.get_values()
image_reves = image_12test.inverse_transform(values)
final = time.time()
print("Tiempo ejecucion image transform = ", final - inicio)
#plt.imshow(image, cmap='gray')
plt.subplots(figsize=(8, 8))
plt.imshow(image_reves, cmap='gray')
plt.xticks([])
plt.yticks([])
plt.show()
print(image_reves.shape)
# Time spent 3.2072246074676514 seg

###Plot over fractal####

"""Fractal emmending"""
m = 0
s = 1/2
size_points = 10
x_position, y_position = Christiakov_emmending(Z_k, m, s)


size = (8, 8)
# plt.figure(figsize=size)
fig, ax = plt.subplots(figsize=size)
fractal = plt.scatter(x_position,
                      y_position,
                      c=values,
                      s=size_points,
                      cmap="gist_gray")


# Setting the background color of the plot
# using set_facecolor() method
ax.set_facecolor('#ADD8E6')
# plt.xticks([])
# plt.yticks([])


plt.show()
