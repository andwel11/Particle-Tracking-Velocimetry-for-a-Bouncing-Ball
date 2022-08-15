#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

author: Angelica Uzo
course: Chemical Engineering
school: University of Birmingham

"""
# This function will produce the displacement, velocity and time of a ping pong ball
# provided the coefficient of restitution e, and dropheight using an empirical model

import numpy as np
import seaborn; seaborn.set_style("whitegrid")

def Empirical(e, dropheight):
    # initial conditions
    # initial vertical displacement
    s_max_down = dropheight
    # initial time
    t0 = 0
    #initial velocity
    v_current = 0
    # Gravitational acceleration
    g = 9.81
    # Coefficient of restitution
    cor = e
    
    # lists are created into which the calculated values will be appended
    s_list = [s_max_down]
    v_list = [0]
    t_list = [t0]
    
    # N defines the number of times the loop is repeated
    N = 0
    while N < 50:
        N = N + 1
        # SUVAT is used for the calculations
        # Calculations when the ball goes up
        t_up = (v_current/g)
        s_max_up = s_max_down  + ((v_current**2) /(2*g))
        v_up = 0
        t_total = t_up + t_list[-1]
        # Appending the calculated values to a list
        s_list.append(s_max_up)
        v_list.append(v_up)
        t_list.append(t_total)             
        
        # Calculations when the ball goes down
        t_down = np.sqrt((2*s_max_up)/g)
        s_max_down = 0
        v_current = (-g*t_down) * -cor
        t_total = t_down + t_list[-1]
        # Appending the calculated values to a list
        s_list.append(s_max_down)
        v_list.append(v_current)
        t_list.append(t_total)  
    # s, v and t are arrays containing the results from the calculations
    s = np.array(s_list)
    v = np.array(v_list)
    t = np.array(t_list)

    return s, v, t


        