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
import time
from skimage.data import camera
p = 3
k = 10
Z_k = Q_p.Z_N_group(p, k)
image = camera()
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
plt.imshow(image_reves, cmap='gray')
print(image_reves.shape)
# Time spent 3.2072246074676514 seg
