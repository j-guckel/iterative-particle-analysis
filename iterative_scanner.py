#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 08:59:43 2022

@author: Jannik Guckel, Daesung Park
"""


import cv2
from PIL import Image, UnidentifiedImageError
import hyperspy.api as hs
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.ndimage import gaussian_filter
import ast
import csv
#needs to be saved in same directory as this file
import os
import shutil
#custom routines
#from subroutines.smart_intensity_criteria import smart_intensity_criteria
from subroutines.enhanced_CHT import enhanced_CHT
from subroutines.logistic_scaling import logistic_scaling
from subroutines.new_image_creator import new_image_creator
from subroutines.binary_mask_maker import binary_mask_maker
#from subroutines.read_input_file import read_input_file

separator = '/' #The separator used in your OS (/ for linux, windows uses \ or different symbol, depending on regional settings of the pc)
#change this value, if you do not use Linux

#print( .... General license information, For detail check the tutorial at *git adress* )

#here insert question to import and input file!
read_input_file = input('Import Parameters from a file? (y/n)')
if read_input_file == 'y': #use pre-made input file!
    exec(open('./subroutines/read_input_file.py').read())
else: #set the parameters on the fly.
    exec(open('./subroutines/set_input_parameters.py').read()) 

full_path = home_path + folder
save_location = home_path + save_folder + folder

while os.path.isdir(home_path + save_folder) == True:
    overwrite = input('Analysis data has been found. Do you wish to overwrite? (y/n) : ')
    if overwrite == 'y':
        break
    if overwrite == 'n':
        save_folder = input('Enter new folder name : ')
        full_path = home_path + folder
        save_location = home_path + save_folder + folder
if os.path.isdir(home_path + save_folder) == False:
    os.mkdir(home_path + save_folder)

try:
    shutil.rmtree(save_location) 
except:
    FileNotFoundError()
os.mkdir(save_location)

exec(open('./subroutines/save_input_params.py').read())


img_series = sorted(glob(('%s*.'+file_format)%(full_path))) 


circle_list_tot = np.empty((0, 4))

for alpha in np.arange(0, len(img_series)): #iteration over different images
    print('analyzing image number', alpha+1, 'of ', len(img_series), ' total images.')
    name = img_series[alpha].split(separator)[-1].split('.')[0]

    try:  #this should work for all "image formats"
        img = Image.open(img_series[alpha]).convert('L') 
    except UnidentifiedImageError: #this should work for raw data formats (such as hdf5 and dm4)
        img = hs.load(img_series[alpha]).data   
        
    orig_img = np.copy(img) 
    
    
    
    img = np.asarray(img)
    
    img = img if data_bar_length == 0 else img[:-data_bar_length, :] 
    
    img = gaussian_filter(img, sigma=gauss_sigma) 
    
    #creation of 8 bit clone for opencv's CHT
    max_grey = np.amax(img)
    
    img = 255/max_grey * img
    img = img.astype(np.uint8) #you need 8 bit image input
    
    
    grey_list = img.ravel()   ###optional thresholding
    if use_top_threshold == True:     
        if type(top_threshold) == int:
            tth = top_threshold          
        if type(top_threshold) == float:
            tq = top_threshold      
            tth = np.quantile(grey_list, tq)    
        img[img>tth] = 0
    
    if use_bottom_threshold==True:     
        if type(bottom_threshold) == int:
            bth = bottom_threshold          
        if type(bottom_threshold) == float:
            bq = bottom_threshold      
            bth = np.quantile(grey_list, bq)    
        img[img<bth] = 0
    
    img = 255 - img if invert_detection_image is True else img
    
    #canny edge image to check edge detection
    CE_IM = cv2.Canny(img, p1/2, p1)
    plt.imsave(save_location + name + '_canny_edge_original.png', CE_IM, cmap = 'gray')
    
    total_binary_mask = np.zeros(img.shape) 
    
    
    new_image = np.copy(img)
    circle_list = np.empty((0, 4))
    
    iteration_num = np.ceil((start_radius - end_radius)/interval_size)
    iterations = np.arange(0, iteration_num, 1)
    
    for i in iterations:   #iteration over radius intervals
        
    
        rmax = int(start_radius - i * interval_size)
        rmin = int(start_radius - (i + 1) * interval_size)
        
        rmin = end_radius if rmin < end_radius else rmin  #prevent detection of circles below previously set minimum radius
        
        print('analzying interval ', int(i+1), 'from ',rmin, 'to ', rmax, 'pixels')
        
        scale = logistic_scaling(rmin, G, a, b, c, d)
        
        p20 = start_factor * 2*np.pi*rmin /scale #make sure that voting threshold decreases with shrinking particle size
        p20 = int(p20)
        lowest_p2 = end_factor * 2*np.pi*rmin  /scale
        lowest_p2 = int(lowest_p2)
        
        p2_early_stop = int(1.5*lowest_p2)
        min_part_dist = min_dist_factor * rmin
        circles = np.empty((1, 4))  #dummy variable
        
        A = (p20 > lowest_p2)
        B = (p20 <= p2_early_stop)
        C = (circles.shape[0] == 0)
        while (A is True and (B and C) is False): # iterative voting threshold reduction
            #submodule enhanced CHT includes smart intensity criteria
            circles = enhanced_CHT(new_image, min_dist=min_part_dist, p1=p1, p2=p20, r1=rmin, r2=rmax, particle_threshold=particle_threshold, use_smart_criteria=use_intensity_criteria)
            binary_mask = binary_mask_maker(new_image, circles)
            new_image = new_image_creator(new_image, binary_mask)
            total_binary_mask = total_binary_mask + binary_mask  #update of binary mask
            
            circles = np.append(circles, alpha* np.ones((circles.shape[0], 1)), axis = 1)
            circle_list = np.append(circle_list, circles, axis = 0)
            
            B = (p20 <= p2_early_stop) 
            C = (circles.shape[0] == 0)
            
            if p20 > lowest_p2:
                p20 -= 1
            
            A = (p20 > lowest_p2) 
            
        total_binary_mask[total_binary_mask > 1] = 1  
        plt.imsave(save_location + name + '_binary_mask'+ 'after_interval_%s'%(rmin) + '_to_%s'%(rmax) + '.png', total_binary_mask)
    
        ce_im = cv2.Canny(new_image, p1/2, p1)
        plt.imsave(save_location + name + '_canny_edge_'+ 'after_interval_%s'%(rmin) + '_to_%s'%(rmax) + '.png', ce_im)
        plt.imsave(save_location + name + '_reduced_image_'+ 'after_interval_%s'%(rmin) + '_to_%s'%(rmax) + '.png', new_image, cmap = 'gray')
    circle_list_tot = np.append(circle_list_tot, circle_list, axis = 0)
    
    fig, ax = plt.subplots(1, 1, num = 3, figsize = (12.8, 12.8))
    ax.imshow(orig_img, cmap = 'gray')
    ax.scatter(circle_list[:, 0], circle_list[:, 1], s = circle_list[:, 2]**2, facecolors = 'none', linewidth = 0.1 * circle_list[:, 2],
               marker = 'o', edgecolors ='r', )    
    tit_02 ='#%s total particles' %(circle_list.shape[0])
    ax.set_title("%s" %(tit_02))        
    plt.savefig(save_location + name + '_iterated_particle_analysis.png')
    plt.close(fig)
    
fig, ax = plt.subplots(1, 1, figsize = (12.8, 9.6))
ax.hist(np.array(2* circle_list_tot[ :, 2])*pixelsize, 10)
tit_01 = '%s' %(2*np.mean(circle_list_tot[:, 2])*pixelsize) + '+- %s' %(2*np.std(circle_list_tot[:,2])*pixelsize) + ', #%s particles'%(circle_list_tot.shape[0]) #
ax.set_title("%s" %(tit_01))
ax.set_xlabel('particle diameter [' + pixel_unit + ']')
plt.tight_layout()
plt.savefig(save_location + #folder +
            'particle_size_distribution.png')
plt.close(fig)

#add the name to the image instead of just image number in iterative series.
index_list = circle_list_tot[:, 3].astype(int)
name_list = [img_series[index_list[i]].split(separator)[-1].split('\n')[0] for i in np.arange(0, index_list.shape[0], 1)]
name_list = np.asarray(name_list)
name_list = name_list.reshape((name_list.shape[0], 1))

#save position of each circle in each image in a table.
with open(save_location + name + '_all_circles_list.csv', 'w', newline = '\n' ) as h:
    writer = csv.writer(h, delimiter =',')
    writer.writerow(['The following coordinates are in image pixels!'])
    writer.writerow(['In order to obtain the real world distances, multiply with the pixelsize of', pixelsize, pixel_unit])
    writer.writerow(['x', 'y', 'R', 'image_num', 'image_name'])
    writer.writerows(np.append(circle_list_tot, name_list, axis = 1))
    h.close()    
    


    