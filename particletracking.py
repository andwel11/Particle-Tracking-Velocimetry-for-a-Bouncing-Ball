#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

author: Angelica Uzo
course: Chemical Engineering
school: University of Birmingham

"""

# This code will track the position of a ball in a video using a function to  
# produce the coefficient of restitution of the ball and plot energy against 
# time as well as vertical displacement against time for the ball.

import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# Start time for the code
start = time.time()

# Function to obtain coefficient of restitution is defined
def particletracking(video_name, b1, t1, k1, min_distance, p1, p2, r_min, r_max, floor, ball_mass, Dropheight):
    # Process video
    cap = cv2.VideoCapture(video_name)
    # Empty lists are created for appending values into it
    y_position = []
    x_position = []
    while True:
        # Extracting the frames
        success, img = cap.read()
        if img is None:
            break
        # Blur the image to remove some noise
        blurred = cv2.blur(img, (b1, b1))
        # Image is converted to greyscale
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        # Greyscale image is then binarized
        _, thresh = cv2.threshold(gray, t1, 255, cv2.THRESH_BINARY)
        # Dilation of the image is carried out to emphasize the circle
        kernel = np.ones((k1, k1), dtype = np.uint8)
        dilation = cv2.dilate(thresh, kernel)
        # Circles present in the image are detected on dilated image
        circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, 1, minDist = min_distance, 
                                   param1 = p1, param2 = p2, minRadius = r_min, maxRadius=r_max)
        if circles is None:
            break
        
        # To view the circles plotted on the images, uncomment lines 53 to 59
        
        # fig, ax = plt.subplots()
        ## Displays the picture dilation
        # ax.imshow(dilation, cmap = "gray")
        ## Adds the drawn circles to the dilated image
        # for circ in circles[0]:
        #     x, y, r = circ
        # ax.add_artist(plt.Circle((x, y), r, fill = False, color = "red"))
        
        # The shape of circles is changed to (1,3)
        circles = circles.reshape(1,3)
        # Append x and y positions to the empty lists
        x_position.append(float(circles[:,0]))
        y_position.append(float(circles[:,1]))
        # To exit the loop
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    # Forming arrays of the entries within list 'x_position' and 'y_position'
    x_distance_in_pixel = np.array(x_position)
    y_distance_in_pixel = np.array(y_position)
    # Obtaining image height
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # Function to convert pixel to metres
    def conversion(distance_in_pixels, dropheight):
        position_from_base = height - distance_in_pixels
        Conversion = dropheight/position_from_base[0]
        position_in_m = position_from_base * Conversion
        return position_in_m
    # Converting x and y to metres
    x_distance_in_m = conversion(x_distance_in_pixel, Dropheight)
    y_distance_in_m = conversion(y_distance_in_pixel, Dropheight)
    
    # Coefficient of restitution
    
    # First minimum value obtained where ball hits ground
    c = [(i) for i, y in enumerate(y_distance_in_m) if y < floor]
    minimum_val = c[0]
    # Obtaining maximum height after 'minimum_val'
    heightafterbounce = max(y_distance_in_m[minimum_val:])
    # Calculating coefficient of restitution
    e = round(abs(np.sqrt(heightafterbounce/Dropheight)), 3)
    print("Coefficient of restitution =", e)
    
    # Obtaining time 
    # Number of frames
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # Frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Determining the duration of the video
    video_time = frame_count/fps
    # Determining the timestep required
    dt = 1/fps
    # 'time' is a matrix starting at 0 and ending at video_time at timestep dt
    time = np.arange(0, video_time, dt)
    
    # Calculating velocity
    change_length = np.array([(y_distance_in_m[i-1]-y_distance_in_m[i]) for i in range (1, len(y_distance_in_m))])
    change_time = np.array([time[i-1]-time[i] for i in range (1, len(y_distance_in_m))])
    velocity = change_length/change_time
    
    # Energy calculations
    # Calculating potential energy
    Ep = ball_mass * 9.81 * (y_distance_in_m[0:-1])
    # Calculating kinetic energy
    Ek = 0.5 * ball_mass * (velocity**2)
    # Calculating total energy
    Et = Ep + Ek
    
    results = [time[0:len(y_distance_in_m)], x_distance_in_m, y_distance_in_m, velocity, Ep, Ek, Et, e, dt, Dropheight, video_time, velocity[0]]
    return (results)

# Select a ball and height to track

# Ping pong ball at 2m
# Data = particletracking("ping pong ball at height 1-1.mp4", 20, 130, 2, 30, 45, 5, 5, 9, 0.6, 0.0027, 2)
# Ping pong ball at 1m
Data = particletracking("ping pong ball at height 2-1.mp4", 12, 130, 2, 30, 50, 5, 5, 9, 0.6, 0.0027, 1)
# Ping pong ball at 0.5m
# Data = particletracking("ping pong ball at height 3-1.mp4", 3, 130, 2, 50, 45, 5, 5, 9, 0.2, 0.0027, 0.5)
# Tennis ball at 1m
# Data = particletracking("tennis ball-1.mp4", 3, 157, 2, 30, 50, 5, 10, 15, 0.15, 0.056, 1)
# Football at 1m
# Data = particletracking("football-1.mp4", 4, 100, 3, 90, 45, 10, 20, 50, 0.6, 0.396, 1)

# Plots
tVals = Data[0]

plt.figure(figsize=(20,30))

# Plotting vertical displacement against time
plt.subplot(3,2,1)
plt.plot(tVals, Data[2],'r.')
plt.xlabel("Time (s)")
plt.ylabel("Vertical displacement (m)")
plt.title("Vertical displacement against time")

# Plotting energy against time
plt.subplot(3,2,2)
plt.plot(tVals[0:-1], Data[5],'r', label="Kinetic energy")
plt.plot(tVals[0:-1], Data[4],'g', label="Potential energy")
plt.plot(tVals[0:-1], Data[6],'k', label="Total energy")
plt.legend(loc="upper right")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.title("Energy against time")


# End time for the code
end = time.time()
# Time taken to execute code
print("Execution took", round(end - start, 3), "s")
