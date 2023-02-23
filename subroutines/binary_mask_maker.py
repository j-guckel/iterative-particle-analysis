#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:09:05 2022

@author: Jannik Guckel, Daesung Park
"""
import numpy as np

def binary_mask_maker(img, circles): #circles in input equals circles from previous output
    binary_mask = np.zeros((img.shape))
    ii, ji = np.ogrid[0: img.shape[0], 0:img.shape[1]]
    for gamma in np.arange(0, circles.shape[0], 1):
            single_mask = (ii - circles[gamma, 1]) ** 2 + (ji - circles[gamma, 0]) ** 2 <= circles[gamma, 2] **2
            binary_mask[single_mask] = 1
    return binary_mask
