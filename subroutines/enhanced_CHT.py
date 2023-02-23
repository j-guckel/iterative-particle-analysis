#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 09:17:20 2022

@author: Jannik Guckel, Daesung Park
"""

import numpy as np
import cv2
from subroutines.smart_intensity_criteria import smart_intensity_criteria


def enhanced_CHT(img,*, min_dist, p1, p2, r1, r2, particle_threshold, use_smart_criteria=True): 
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, min_dist, param1 = p1, param2 = p2, minRadius = r1, maxRadius = r2)
    
    circles = np.empty((1, 0, 3)) if circles is None else circles
    circles = circles[0]
    
    duplicate_list = []
    if use_smart_criteria is True: #disabling this option disables our smart intensity criteria
        
        
        s = int(np.round(0.1*r1))  
        
        s = 1 if s < 1 else s  #ensure that s will not go below 1.
        
        duplicate_list = smart_intensity_criteria(img, circles, s, particle_threshold)
        
        
    circles = np.delete(circles, duplicate_list, axis = 0)
    
    return circles
    
