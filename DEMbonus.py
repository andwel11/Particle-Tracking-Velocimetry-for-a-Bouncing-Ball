"""

author: Angelica Uzo
course: Chemical Engineering
school: University of Birmingham

"""

# This function will produce the displacement, velocity and time of a ping pong ball with drag and buoyancy acting 
# on it travelling through air provided the coefficient of restitution e, timestep, dropheight, final time,
# velocity, diameter and mass respectively using a DEM model (Euler method)
import numpy as np
import seaborn; seaborn.set_style("whitegrid")

def DEM(e, timestep, y, tmax, velocity, d, m):
    # Pre-defined parameters
    # Initial position
    rx0 = 0 #m
    ry0 = y #m
    
    # Initial speed and angle of inclination to the horizontal
    v0 = velocity #m s^-1
    theta = 0 #in degrees
    
    # Gravitational acceleration
    g = 9.81 #m s^-2
    
    # Initial time
    t0 = 0 #s
    
    # Coefficient of restitution
    cor = e #dimensionless 
    
    # Density
    rho_air = 1.225 #kg m^-3 for the fluid
    
    # Ping pong ball dimensions
    radius = d/2 #m
    cd = 0.47 #drag coefficient (dimensionless)
    # The projected area of a sphere is a circle
    projected_area = np.pi * radius ** 2 #m^2
    volume = np.pi * 4 / 3 * radius ** 3 #m^3
    mass = m
    
    # User-defined parameters
    # Time step                          
    dt = timestep #s
    # Final time
    tf = tmax #s 
    
    # Buoyancy
    force_buoyancy = rho_air * volume * g
    
    # This fuction returns the drag force at the velocity stated
    def drag_force(velocity):
        drag = 0.5 * cd * projected_area * rho_air * velocity ** 2 
        return drag
    
    # t_current represents the time at the current position of the projectile
    t_current = t0
    
    # r_current_drag is an array containing the current horizontal and vertical displacements of the projectile
    r_current_drag = np.array([rx0 , ry0]) 
    
    # v_current_drag is an array containing the current horizontal and vertical velocities of the projectile
    v_current_drag = np.array([v0 * np.cos(np.radians(theta)) , v0 * np.sin(np.radians(theta))])
    
    # position_drag, time and speed_drag represent empty lists into which the r_current_drag, 
    # t_current and v_current_drag values will be appended
    position_drag = []
    speed_drag = []
    time = []
    
    # Euler's Method
    # This loop calculates r_current_drag and v_current_drag at t_current and 
    # appends it to the list 'position_drag' and 'speed_drag' respectively 
    # until t_current is equal to tf after which the loop is terminated.  
    while t_current <= tf:
        # Calculating acceleration
        v0_magitude = np.sqrt(v_current_drag[0]**2 + v_current_drag[1]**2)
        a_drag = np.array([1 / mass * drag_force(v_current_drag[0]) * (-v_current_drag[0]/v0_magitude), 
                          - g + 1 / mass * drag_force(v_current_drag[1]) - force_buoyancy / mass * (-v_current_drag[1]/v0_magitude)])
        # r_current_drag[0] represents the vertical displacement, r_current_drag[1] represents the horizontal displacement
        # v_current_drag[0] represents the vertical velocity, v_current_drag[1] represents the horizontal velocity
        v_new_drag = np.array([v_current_drag[0] + dt * a_drag[0] , v_current_drag[1] + dt * a_drag[1]])
        r_new_drag = np.array([r_current_drag[0] + v_current_drag[0] * dt , r_current_drag[1] + v_current_drag[1] * dt])
        # 'position_drag.append(r_current_drag)' modifies the list 'position_drag' by adding r_current_drag to the end of the list 
        # rx_and_ry_drag represents an array of the entries within 'position_drag'
        position_drag.append(r_current_drag)
        rx_and_ry_drag = np.array(position_drag)
        # This modifies the list 'speed_drag' by adding v_current_drag to the end of the list 
        # v_drag represents an array of the entries within 'speed_drag'
        speed_drag.append(v_current_drag)
        v_drag = np.array(speed_drag)
        # The 'if' conditional statement below accounts for the bounce
        if r_new_drag[1] < 0:
             v_new_drag[1] = -cor * v_current_drag[1]
             r_new_drag[1] = 0  
        # r_new_drag and v_new_drag become the next timestep's r_current_drag and v_current_drag values
        v_current_drag = v_new_drag
        r_current_drag = r_new_drag
        # t represents an array of the entries within time
        time.append(t_current)
        t = np.array(time)
        # This defines t_current at the new timestep and the loop repeats
        t_current = t_current + dt
            
        
    return rx_and_ry_drag, v_drag, t
        
