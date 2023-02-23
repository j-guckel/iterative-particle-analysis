#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:38:21 2022

@author: Jannik Guckel, Daesung Park
"""

import csv

with open(save_location + "_input_params.txt", "w", newline="\n" ) as g:
            writer = csv.writer(g, delimiter =',')
            writer.writerow(['[Program Information]'])
            writer.writerow(['program version: 1.0 initial release'])
            
            writer.writerow(['[Data Information]'])
            writer.writerow(['Home Directory of Data: '])
            writer.writerow([home_path.split('\n')[0]])
            writer.writerow(['Relative Working Directory of the Data Subset:'])
            writer.writerow([folder.split('\n')[0]])
            writer.writerow(['Name of Results Folder: '])
            writer.writerow([save_folder.split('\n')[0]])
            writer.writerow(['Data Format: '])
            writer.writerow([file_format.split('\n')[0]])
            writer.writerow(['Pixel Size: '])
            writer.writerow([pixelsize])
            writer.writerow(['Unit of Pixel size: '])
            writer.writerow([pixel_unit.split('\n')[0]])
            
            writer.writerow(['[Detection Parameters]'])
            writer.writerow(['Canny Edge Detection Threshold p1 (8-bit unsigned integer) '])
            writer.writerow([p1])
            writer.writerow(['Max Radius (pixel): '])
            writer.writerow([start_radius])
            writer.writerow(['Min Radius (pixel): '])
            writer.writerow([end_radius])
            writer.writerow(['Radius Interval Size (pixel): '])
            writer.writerow([interval_size])
            writer.writerow(['Particle Overlap Factor P (no unit) - minimum distance between neighboring particles = P * r: '])
            writer.writerow([min_dist_factor])
            writer.writerow(['Initial Proportional Factor c1 (no unit): '])
            writer.writerow([start_factor])
            writer.writerow(['Lower Limit Proportional Factor c2 (no unit): '])
            writer.writerow([end_factor])
            writer.writerow(['Upper Limit of Logistic Function G: '])
            writer.writerow([G])
            writer.writerow(['Lower Limit of Logistic Function a: '])
            writer.writerow([a])
            writer.writerow(['Difference Parameter of Logistic Function b (= G - a): '])
            writer.writerow([b])
            writer.writerow(['Convergence Speed Parameter of Logistic Function c: '])
            writer.writerow([c])
            writer.writerow(['Low Pixel Regime Threshold of Logistic Function d: '])
            writer.writerow([d])
            writer.writerow(['use intensity criteria (bool): '])
            writer.writerow([use_intensity_criteria])
            writer.writerow(['particle threshold (8 bit gray): '])
            if use_intensity_criteria is True:
                writer.writerow([particle_threshold])
            else:
                writer.writerow([0])
            
            
            
            writer.writerow(['[Pre-Processing Parameters]'])
            writer.writerow(['Standard Deviation Gaussian Blurring (no unit): '])
            writer.writerow([gauss_sigma])
            writer.writerow(['Databar Length (Pixel): '])
            writer.writerow([data_bar_length])
            writer.writerow(['Constrast Inversion (bool): '])
            writer.writerow([invert_detection_image])
            writer.writerow(['Use Bottom Threshold (bool): '])
            writer.writerow([use_bottom_threshold])
            writer.writerow(['Bottom Threshold: '])
            if use_bottom_threshold is True:
                writer.writerow([bottom_threshold])
            else:
                writer.writerow([0.0])
                
            writer.writerow(['use Top Threshold (bool): '])
            writer.writerow([use_top_threshold])
            writer.writerow(['Top Threshold: '])
            if use_top_threshold is True:
                writer.writerow([top_threshold])
            else:
                writer.writerow([1.0])
            
            g.close()
