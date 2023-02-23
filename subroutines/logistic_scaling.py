#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:07:26 2022

@author: Jannik Guckel, Daesung Park
"""

import numpy as np


def logistic_scaling(x, G, a, b, c, d):
    # this function is supposed to be a scaling function for the voting threshold.
    # instead of threshold = const * 2pi r, threshold = const * 2pi r / scaling (r) is supposed to be used.
    #explanation of function: logistic function is monotonous and positive.
    # the variable x is supposed to stand for the minimum radius of the interval
    # at x = infinite, the functions goes towards G/a
    #assuming d = 0, at x = 0, the function assumes the value of G/(a + b)
    #for a  = 1, b = G - 1, this results in a range from 1 to G, at monotonous growth with x
    # The factor 0 < c < 1 stretches the function in x-direction, slowing down the growth
    # d > 0 shifts the function to the left on the x-axis. (x-d) < 0 results in logistic values between 0 and 1.
    # this would cause the initial assumed scaling of "const * 2pi r" to grow instead of shrinking. to prevent this, the value of scaling (r) is set to 0 if r < d 
    # the values of a = 1 and b = G-1 are supposed to be fixed.
    # G and c need to be fine tuned, but once set they are not meant to be customized by default.
    
    denominator = a + b *np.exp(-c * (x - d))
    logistic = G/denominator
    logistic = 1 if (x-d) < 0 else logistic   # this ensures that for x < d, the scaling cannot drop below 1.
    return logistic
