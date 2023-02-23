#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 10:55:24 2022

@author: Jannik Guckel, Daesung Park
"""
import ast

home_path = input('Working directory of your data. Absolute path is preferred. Make sure the directory ends on a separator (e.g. /) for Linux : ')
folder = input('Relative Path to a folder within the working directory. The images located in this folder will be analyzed. Make sure to include the separator : ')
full_path = home_path + folder
save_folder = input('Name of the folder, where the data will be saved. This folder will be located on the plane of the working directory. Separator must be included. WARNING: Leaving this empty may overwrite your original data! : ')
save_location = home_path + save_folder + folder

file_format = input('name of the file format you wish to analyze (without the . in front of it). tested formats: png, jpeg, tif, dm4, hdf5 : ')
    
pixelsize = float (input('size of a pixel (Square Pixel). Unit will be asked in the next question : ') )
pixel_unit = input('Unit of the Pixel Size, e.g. nm : ')
    
print('We use OpenCVs CHT for analysis. Therefore we temporarily convert the image into 8-bit. Intensity values should therefore be chosen with this in mind : ')
p1 = int( input('Gradient Threshold for Canny Edge filter of OpenCV. Integer Values between 0 and 255 are allowed, as OpenCV works in 8-bit : ') )
    
start_radius = int( input('Maximum estimated radius of the investigated particles (in Pixels, integer) : ') )
end_radius = int( input ('Minimum estimated radius of the investigated particles (in Pixels, integer) : ') )
interval_size = int( input('Interval Size in Pixels. We assume uniform intervals (integer) : ') )
    
invert_detection_image = bool (input('Are the particles darker than the background? (1 for yes, 0 for no) : '))
    
use_intensity_criteria = bool( input('Do you want to include intensity criteria? (0 for no, 1 for yes) : ') )
particle_threshold = int ( input ('Particle Intensity threshold (integer values between 0 and 255 in 8 bit) : ') ) if use_intensity_criteria is True else 0
    
use_additional_options = input('Customize other parameters? (y/n) Choosing n will use default parameters : ')
    
#default parameters of program. These are used if the option no is selected.
gauss_sigma = 2  
data_bar_length = 0
start_factor = 0.5
end_factor = 0.15
min_dist_factor = 1.5
#parameters for logistic function
G = 3
a = 1
b = G - a
c = 0.1
d = 12
#Thresholding parameters
use_top_threshold = False
use_bottom_threshold = False
       
top_threshold = 1.0
bottom_threshold = 0.0
    
    
if use_additional_options == 'y':
        modify_image_preprocessing = input('Modify pre-processing routines? (y/n) : ')
        modify_scaling_factors = input('Modify default values for Scaling function? (y/n) : ')
        apply_thresholding = input('Do you want to apply intensity thresholding to the images? (y/n), default n : ')
       
        
        gauss_sigma = float( input('Standard deviation of a Gaussian Kernel for optional Despiking. Choosing 0 disables this option. : ') ) if modify_image_preprocessing == 'y' else gauss_sigma
        data_bar_length = int( input('Height of the data bar in pixel (integer). This will remove the bottom rows of the image. Choosing 0 will disable this. : ') ) if modify_image_preprocessing == 'y' else data_bar_length
        start_factor = float ( input('Linear Scaling coefficient to determine the starting voting threshold (c1 in Paper) : ') ) if modify_scaling_factors == 'y' else start_factor
        end_factor = float ( input('Linear Scaling coefficient to determine the bottom voting threshold (c2 in Paper : ') ) if modify_scaling_factors == 'y' else end_factor
        G = float (input ('Value of upper limit G of logistic function : ') ) if modify_scaling_factors =='y' else G
        a = 1
        b = G - a
        c = float( input ('Growth speed of logistic function c : ') ) if modify_scaling_factors == 'y' else c
        d = int (input ('Threshold between low and medium pixel regime d : ')) if modify_scaling_factors == 'y' else d
        use_top_threshold = bool( ast.literal_eval( input('Do you want to apply top thresholding? (1 for yes, 0 for no). WARNING: Thresholding is applied before a potential contrast inversion! : ') ) ) if apply_thresholding == 'y' else use_top_threshold
        use_bottom_threshold = bool ( ast.literal_eval (input('Do you want to apply bottom thresholding? (1 for yes, 0 for no). WARNING: Thresholding is applied before a potential contrast inversion! : ') ) ) if apply_thresholding == 'y' else use_bottom_threshold
        top_threshold = ast.literal_eval (input ('Enter top threshold value. Float values between 0.0 and 1.0 will use the respective gray value quantile, integer values will use an absolute gray value (between 0 and 255) : ') ) if use_top_threshold is True else 1.0
        bottom_threshold = ast.literal_eval (input ('Enter bottom threshold value Float values between 0.0 and 1.0 will use the respective gray value quantile, integer values will use an absolute gray value (between 0 and 255) : ') ) if use_bottom_threshold is True else 0.0
        
