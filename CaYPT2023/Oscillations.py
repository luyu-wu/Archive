import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# modes

angletime = False


# Parameters
timestep = 0.001
graph_time = 7  # Amount of time to graph in seconds
slowmotion = 1  # Time Advancer, 2 = 2x slower. 1 is theoretical real time.

"""Experimental Values
slope = np.radians(10.10) # Theta
Theta = np.radians(-180) # Starts at 0 degrees on the sin circle. Goes under Y Axis, so becomes negative in oscillation.
theta_cone = np.radians(8.8) # Theta of the cone, where the parallel axis of rotation lies
mass = 0.02 # Kilograms
length = 20.2/100 # Meters. Eneter value in centimeteres.
thread_position = 0.56
com = 0.9 # Center of mass.. All forces are applied to this. This calculated in relationship to the origin point of where the cone oscillates.
"""

slope = np.radians(30)  # Theta
Theta = np.radians(
    -180
)  # Starts at 0 degrees on the sin circle. Goes under Y Axis, so becomes negative in oscillation.
theta_cone = np.radians(
    15
)  # Theta of the cone, where the parallel axis of rotation lies
mass = 0.02  # Kilograms
length = 20.2 / 100  # Meters. Eneter value in centimeteres.
thread_position = 0.56
com = 0.9  # Center of mass.. All forces are applied to this. This calculated in relationship to the origin point of where the cone oscillates.


gravity = 9.8  # Gravitational Acceleration
friction_coef = 0.4  # Friction Coefficient, Experimentally Found
rotational_fraction = 20  # Friction Coefficient divided by this is the rotational friction coefficient. Experimentally found.
static_friction = 0.05  # Coefficient of normal force to find the critical threshhold of static friction.

# Derived Variables
grav_f = 9.8 * mass
friction = grav_f * friction_coef


thread_diam = np.tan(theta_cone) * length * thread_position
head_diam = np.tan(theta_cone) * length  # Diameter of head 我是一个小小的迷路人
side_length = np.sqrt(head_diam**2 + length**-2)
head_circ = np.pi * head_diam  # Circumference
com_rad = (head_diam * com) / 2
com_circ = length * com * 2 * np.pi

# FORCES

downwards_force = np.cos(slope) * grav_f
forwards_force = np.sin(slope) * grav_f

downwards_force = (
    grav_f - downwards_force
)  # POSITIVE MAGNITUDE OF FORCE. Includes gravity. Gravitational Force is always larger than or equal to.

# Normalize forces to slope angles.
forwards_force = (np.sin(slope) * downwards_force) + (
    np.cos(slope) * forwards_force
)  # Forwads backwards in relation to board direction.
downwards_force = (np.cos(slope) * -downwards_force) + (
    np.sin(slope) * forwards_force
)  # Up down direction


# Positioning Data


def FindY(Angle):
    return np.sin(slope) * com * length * np.sin(Angle) + com_rad * np.cos(slope)


lowestY = FindY(
    -90
)  # Highest and lowest point where 0 is the binding point of the cone.
highestY = FindY(Theta)
a_velocity = 0  # Angular velocity.


x_velocity = 0  # Affected only by centrifugal and friction
y_velocity = 0  # Affected by Gravity, Centrifugal, and Friction


g_potent = grav_f * (
    highestY - lowestY
)  # Equivalent to mgh. Calculated relative to lowest point com will reach.
x, y = 0, 0


print("Gravitation Potential Energy: ", g_potent)


# [[ SIMULATION ]] #

# I treat velocity forming the oscillation and movement of the screw differently. Shouldn't make a difference as you can just superimpose.
graph = []

break_static = []

broke_Static = False


for _ in range(int(graph_time / timestep)):
    parallel_vector = np.cos(Theta) * forwards_force  # Newtons
    purpendicular_vector = np.abs(
        np.sin(Theta) * forwards_force
    )  # Force that goes into breaking static friction. Newtons.

    centrifugal = (
        mass * length * com * (2 * np.pi * (a_velocity / com_circ)) ** 2
    )  # In Newtons, this force is directly purpendicular to the screw head.

    centrifugal_x = np.cos(Theta) * centrifugal
    centrifugal_y = np.sin(Theta) * centrifugal

    break_static.append(purpendicular_vector + centrifugal)
    # Forces
    if not broke_Static:
        a_velocity -= (
            (parallel_vector) / mass
        ) * timestep  # Acceleration multiplied by time to change the velocity.

        if a_velocity != 0:
            direction = a_velocity / np.abs(a_velocity)

            a_velocity -= (
                ((friction / rotational_fraction) / mass) * timestep * direction * 2
            )

        Theta += (
            2 * np.pi * (a_velocity / com_circ)
        ) * timestep  # Change Theta based upon the calculated angular velocity.

        if (
            purpendicular_vector + centrifugal
            > grav_f * friction_coef * static_friction
        ):
            broke_Static = True
    else:
        nonr_x = (
            np.cos(Theta) * purpendicular_vector + centrifugal_x
        )  # The forces purpendicular to screw head put back into ramp space.
        nonr_y = np.sin(Theta) * purpendicular_vector + centrifugal_y

        angular_y = (
            np.cos(Theta) * a_velocity
        )  # Forces that apply to the angular velocity
        angular_x = np.sin(Theta) * a_velocity

        y_velocity += ((nonr_y) / mass) * timestep

        if y_velocity != 0:
            # Friction opposes direction, so we need the current direction of the Y movement.
            direction = y_velocity / np.abs(y_velocity)

            # Kinetic Friction can only be applied via the head direction in local screw space.
            y_velocity += (
                np.sin(Theta) * ((friction * 0.5) / mass) * timestep * direction
            )
            # print(y_velocity<0)

        x_velocity += (nonr_x / mass) * timestep

        if x_velocity != 0:
            # Friction opposes direction, so we need the current direction of the X movement.
            direction = x_velocity / np.abs(x_velocity)

            # Kinetic Friction can only be applied via the head direction in local screw space.
            x_velocity -= (np.cos(Theta)) * (friction / mass) * timestep * direction

        a_velocity -= (
            ((parallel_vector) / mass) * timestep
        )  # Acceleration multiplied by time to change the velocity. Metres per Second

        if a_velocity != 0:  # Dampening Factor for Oscillation
            direction = a_velocity / np.abs(a_velocity)

            a_velocity -= (
                ((friction / rotational_fraction) / mass) * timestep * direction
            )

        Theta += (
            2 * np.pi * (a_velocity / com_circ) * timestep
        )  # Change Theta based upon the calculated angular velocity.

        y += y_velocity * timestep
        x += x_velocity * timestep

    for i in range(slowmotion):
        graph.append([Theta, x, y])

print("Bottom Y:", y)
# PLOTTING

plt.xlabel("Time (ms)")
plt.ylabel("Theta (Radians)")
# plt.show()
plt.plot(break_static)


graph_size = 60
if angletime:
    graph2 = []
    for i in graph:
        graph2.append(i[0] + (np.pi / 2))
    plt.axes(xlim=(0, graph_time / timestep), ylim=(-2, 2))
    plt.plot(graph2)

    plt.xlabel("Time (ms)")
    plt.ylabel("Theta (Radians)")
    plt.show()
else:
    plt.style.use("dark_background")

    fig = plt.figure()
    ax = plt.axes(xlim=(-graph_size / 2, graph_size / 2), ylim=(0, graph_size))
    (line,) = ax.plot([], [], lw=3)
    (head,) = ax.plot([], [], lw=2)

    def init():
        # creating an empty plot/frame
        line.set_data([], [])
        return (line,)

    def animate(i):
        print(
            "Compiling:",
            math.floor((i / (graph_time * 30 * slowmotion)) * 1000) / 10,
            "%",
        )
        Coordinates = graph[np.clip(i * 30, 0, len(graph) - 1)]
        Frame = Coordinates[0]

        x_vector = np.cos(Frame)

        y_vector = np.sin(Frame)
        xdata, ydata = (
            [
                (length * 100 * thread_position * x_vector) + Coordinates[1],
                (length * 100 * x_vector) + Coordinates[1],
            ],
            [
                graph_size * 0.95
                + (length * 100 * thread_position * y_vector)
                + Coordinates[2],
                graph_size * 0.95 + (length * 100 * y_vector) + Coordinates[2],
            ],
        )

        xdatah, ydatah = (
            [
                xdata[1] + np.sin(Frame) * (head_diam * 50),
                xdata[1] - np.sin(Frame) * (head_diam * 50),
            ],
            [
                ydata[1] - np.cos(Frame) * (head_diam * 50),
                ydata[1] + np.cos(Frame) * (head_diam * 50),
            ],
        )
        line.set_data(xdata, ydata)

        head.set_data(xdatah, ydatah)
        return line, head

    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=int(graph_time * 30 * slowmotion),
        interval=np.floor(1000 / 30),
        blit=True,
    )

    # line = plt.plot(graph)

    plt.xlabel("Position X (cm)")
    plt.ylabel("Position Y (cm)")
    # plt.show()

    anim.save("Oscillations.gif", writer="pillow")
