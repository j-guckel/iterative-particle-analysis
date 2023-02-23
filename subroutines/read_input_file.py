#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:31:24 2022

@author: Jannik Guckel, Daesung Park
"""

import ast

ipf = input('Path to Input File  (Including Name and Ending): ')

parameter_file = open(ipf).readlines()

#Split Lines into Different Sub-Blocks
Block1_Start = parameter_file.index('[Program Information]\n')
Block2_Start = parameter_file.index('[Data Information]\n')
Block3_Start = parameter_file.index('[Detection Parameters]\n')
Block4_Start = parameter_file.index('[Pre-Processing Parameters]\n')
#make subset for each block
Block1 = parameter_file[Block1_Start+1:Block2_Start]
Block2 = parameter_file[Block2_Start+1:Block3_Start]
Block3 = parameter_file[Block3_Start+1:Block4_Start]
Block4 = parameter_file[Block4_Start+1:]

#Analysis of Block 2:
home_path = Block2[1].split('\n')[0]
folder = Block2[3].split('\n')[0]
save_folder = Block2[5].split('\n')[0]
file_format = Block2[7].split('\n')[0]
pixelsize = ast.literal_eval(Block2[9])
pixel_unit = Block2[11].split('\n')[0]

#Analysis of Block 3:
p1 = ast.literal_eval(Block3[1])
start_radius = ast.literal_eval(Block3[3])
end_radius = ast.literal_eval(Block3[5])
interval_size = ast.literal_eval(Block3[7])
min_dist_factor = ast.literal_eval(Block3[9])
start_factor = ast.literal_eval(Block3[11])
end_factor = ast.literal_eval(Block3[13])
G = ast.literal_eval(Block3[15])
a = ast.literal_eval(Block3[17])
b = ast.literal_eval(Block3[19])
c = ast.literal_eval(Block3[21])
d = ast.literal_eval(Block3[23])
use_intensity_criteria = ast.literal_eval(Block3[25])
particle_threshold = ast.literal_eval(Block3[27])

#Analysis of Block 4:
gauss_sigma = ast.literal_eval(Block4[1])
data_bar_length = ast.literal_eval(Block4[3])
invert_detection_image = ast.literal_eval(Block4[5])
use_bottom_threshold = ast.literal_eval(Block4[7])
bottom_threshold = ast.literal_eval(Block4[9])
use_top_threshold = ast.literal_eval(Block4[11])
top_threshold = ast.literal_eval(Block4[13])



