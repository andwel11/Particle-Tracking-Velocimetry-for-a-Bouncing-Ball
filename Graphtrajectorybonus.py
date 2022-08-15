"""

author: Angelica Uzo
course: Chemical Engineering
school: University of Birmingham

"""
# This code will call all three functions: particletracking, empirical and DEM 
# and plot the results on a graph

from particletracking import particletracking
from DEMbonus import DEM
from Empiricalbonus import Empirical
import matplotlib.pyplot as plt


# Ping pong ball at 1m
Data = particletracking("ping pong ball at height 2-1.mp4", 12, 130, 2, 30, 50, 5, 5, 9, 0.6, 0.0027, 1)
r, v, t = DEM(Data[7], Data[8], Data[9], Data[10], Data[11], 0.040, 0.004)
s_emp, v_emp, t_emp = Empirical(Data[7], Data[9])

# Plots
# There is a need to crop the plots as there are about 6 staionary points in the 
# displacemets when the ball was held at the start of the video before it was allowed to bounce
tVals = Data[0]
newt = tVals[:-6]

y_proj = Data[2]
newy = y_proj[6:]

v_proj = Data[3]
newv = v_proj[6:]

plt.figure(figsize=(20,10))

# Plotting vertical displacement against time
plt.subplot(1,2,1)
plt.plot(newt, newy,'r.', label="Actual")
plt.plot(t, r[:,1],'k', label="DEM")
plt.plot(t_emp, s_emp,'b', label="Empirical")
plt.xlim(0, 4.1)
plt.legend(loc="upper right")
plt.xlabel("Time (s)")
plt.ylabel("Vertical displacement (m)")
plt.title("Vertical displacement against time")

# Plotting energy against time
plt.subplot(1,2,2)
plt.plot(newt[1:], newv,'g.', label="Actual")
plt.plot(t, v,'b', label="DEM")
plt.plot(t_emp, v_emp,'r.', label="Empirical")
plt.xlim(0, 4)
plt.legend(loc="upper right")
plt.xlabel("Time (s)")
plt.ylabel("Velocity ($ms^{-1}$)")
plt.title("Velocity against time")
