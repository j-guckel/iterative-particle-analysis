#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:08:00 2022

@author: Jannik Guckel, Daesung Park
"""

import numpy as np

def new_image_creator(img, binary_mask): #create new image from binary mask
    new_img = img - binary_mask * img
    new_img[new_img < 0] = 0
    new_img = new_img.astype(np.uint8)
    return new_img
