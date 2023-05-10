![matrix](https://github.com/yago-mendoza/herding-sim/blob/main/images/matrix.gif)

# Herding-Sim

[![license: MIT](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)

Herding-Sim is a dynamic simulation playground designed for training agents using Q-Learning algorithms. The environment is composed of particles that adhere to realistic physical behaviors, allowing for comprehensive training scenarios. To achieve this purpose, additional architectures can be programmed to control the repelling point in pursuit of specific training objectives. The mechanics are highly flexible and scalable, enabling users to exercise control over the constituent elements to suit specific training goals.

## Execution

To engage with the simulation, Python and Pygame must be pre-installed on the local device.

After installation, run the following command.

```python
py .\boid_modeling.py
```

## Mechanics

The user can control the movement of the repelling point using the mouse or arrow keys, which changes its position in the simulation environment. As the repelling point moves, its influence on the particles within the environment also changes, causing them to move away from the repelling point and potentially interact with other particles in the environment. This interactive feature provides a more engaging and dynamic simulation experience for the user, as they can actively participate in the simulation by controlling the repelling point and observing the resulting behavior of the particles in the environment.

### Controls
#### Visualization
* Press **`a`** to draw accelerations
* Press **`v`** to draw velocities
* Press **`d`** to draw the dog's repulsion range
* Press **`c`** to identify the clusters of sheep
* Press **`k`** to show the indexes of sheep
* Press **`s`** to display clusters' statistics (momentum and count)
#### Control
* Press **`←`** to drive the dog left
* Press **`→`** to drive the dog right
* Press **`↑`** to drive the dog up
* Press **`↓`** to drive the dog down

## About the program

Herding-Sim is written in Python using the Pygame library to handle the graphical user interface. The program's code structure consists of a series of flow structures and Pygame functions. Pygame is declared as a global variable and used throughout the code. The program begins by initializing Pygame and setting up the display window. Next, the program sets up the simulation environment and creates the boid particles, assigning each particle its unique characteristics.

### Simulation parameters
The simulation can be customized with several parameters to configure the behavior of the particles, including:
* **`num_sheep`**: the number of sheep in the simulation.
* **`spawn_radius`**: the radius of the circle in which the sheep are spawned.
* **`spawn_width`**: the width of the circle in which the sheep are spawned.
* **`spawn_top_speed`**: the maximum speed that a sheep can have when spawned.
* **`max_sheep_speed`**: the maximum speed that a sheep can have.
* **`dog_x, dog_y`**: the initial position of the dog.
* **`dog_speed`**: the speed of the dog.
* **`sheep_attraction_range`**: the range within which the sheep are attracted to each other.
* **`dog_repulsion_range`**: the range within which the sheep are repelled by the dog.
* **`wall_repulsion_factor`**: the factor by which the sheep are repelled by the walls of the screen.
* **`sheep_repulsion_factor`**: the factor by which the sheep are repelled by each other.
* **`dog_repulsion_factor`**: the factor by which the sheep are repelled by the dog.

These parameters enable users to customize the simulation to their specific needs, allowing for a wide range of training scenarios and experiments.

The simulation itself is run within a while loop that continuously updates the positions and behaviors of the particles. The loop also checks for user input and updates the display accordingly. Additionally, the program includes several functions for calculating various aspects of the boid particles' behavior.

#### Kinematics

The code calculates the net acceleration experienced by each sheep based on various factors in their environment such as:

- **(`a_friction_x`, `a_friction_y`)** represent terrain resistance and are calculated based on the current velocity of the sheep. They help prevent the sheep from running endlessly by gradually slowing them down over time.
- **(`a_center_x`, `a_center_y`)** are used to simulate attraction to other sheep and enable flocking behavior. They are calculated based on the distance between each sheep and its neighbors and their relative velocities. The closer the sheep are to each other, the stronger the attraction force.
- **(`a_static_x`, `a_static_y`)** are used to simulate repulsion from other sheep and avoid stacking. They are calculated based on the distance between each sheep and its neighbors, their relative velocities, and a repulsion factor. The closer the sheep are to each other, the stronger the repulsion force.
- **(`a_dog_x`, `a_dog_y`)** represent the repulsion force from the dog and are calculated based on the distance between each sheep and the dog. The closer the sheep are to the dog, the stronger the repulsion force.
- **(`a_wall_x`, `a_wall_y`)** represent the repulsion force from walls and are set to 0 by default.

This net acceleration is then used to update the velocity components using the MRUA equations. The code checks whether the speed limit for each sheep has been exceeded and corrects it if necessary by setting the velocity component to the maximum speed limit while maintaining its direction.

```python
        a_x[k] = a_friction_x + a_center_x + a_static_x + a_dog_x + a_wall_x
        a_y[k] = a_friction_y + a_center_y + a_static_y + a_dog_y + a_wall_y

        v_x[k] = v_x[k] + a_x[k]*t_s
        v_y[k] = v_y[k] + a_y[k]*t_s

        a_x[k] = max_sheep_speed if (abs(a_x[k])) > max_sheep_speed else a_x[k]
        a_y[k] = max_sheep_speed if (abs(a_y[k])) > max_sheep_speed else a_y[k]

        p_x[k] = p_x[k] + v_x[k]*t_s + 0.5*a_x[k]*t_s**2
        p_y[k] = p_y[k] + v_y[k]*t_s + 0.5*a_y[k]*t_s**2
```

Note that this code uses vectors to represent sheep instead of classes to optimize performance and reduce memory usage. This approach simplifies the code and makes it more efficient, especially when simulating large numbers of sheep.

-----

![test](https://github.com/yago-mendoza/herding-sim/blob/main/images/test.gif)

