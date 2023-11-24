# modules
import matplotlib.pyplot as plt
import numpy as np
# Mutables
vx = 0 # velocity
accel = 0
distance = 0.8 # position
position_table = []
time_table = []

# Adjustables

k = 10 # Nm
mass = 1 # kg
timestep = 0.1
time = 0
repeats = 100

# Main Body
for i in range(repeats):
    accel = (distance*k)*timestep
    vx = vx + (accel/mass)*timestep
    # vx = vx*0.99 # Dampening
    distance = distance - (vx*timestep)
    time = time + timestep

    position_table.append(distance)
    time_table.append(time)

plt.plot(np.array(time_table), np.array(position_table))
plt.show()
