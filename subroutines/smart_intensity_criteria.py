#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:09:53 2022

@author: Jannik Guckel, Daesung Park
"""

import numpy as np

def smart_intensity_criteria(img, circles, contour_width, particle_threshold):

    ii, ji = np.ogrid[0: img.shape[0], 0:img.shape[1]]
    duplicate_list = []
    
    for gamma in np.arange(0, circles.shape[0], 1):
            circle_mask = (ii - circles[gamma, 1]) ** 2 + (ji - circles[gamma, 0]) ** 2 <= circles[gamma, 2] **2
            

            #determine the inside of a particle
            roll_1 = np.roll(circle_mask, axis = 1, shift = contour_width) 
            roll_2 = np.roll(circle_mask, axis = 1, shift = -1*contour_width) 
            roll_3 = np.roll(circle_mask, axis = 0, shift = contour_width) 
            roll_4 = np.roll(circle_mask, axis = 0, shift = -1*contour_width)
            
            contour_mask = circle_mask & ~(roll_1 & roll_2 & roll_3 & roll_4) #particle contour
                        
            avg_particle_intensity = np.mean(img[circle_mask]) #inside intensity
            
            avg_contour_intensity = np.mean(img[contour_mask]) #contour intensity
            
            real_pixels = np.count_nonzero(img[circle_mask] > 0) #count how many zeros are inside
            
            cond1 = avg_particle_intensity < particle_threshold  #inside the particle needs to be a specific brightness
            cond2 = real_pixels < 0.75*np.pi*circles[gamma, 2]**2 # a particle counts as duplicate, if too many pixels inside the circle are 0
            cond3 = avg_contour_intensity < 0.5*particle_threshold #The contour also needs to pass the brightness criterion
            
            if  np.any([cond1, cond2, cond3]) == True : 
                duplicate_list.append(gamma)
    
    return duplicate_list
