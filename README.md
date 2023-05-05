# Herding-Sim

[![license: MIT](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)

This repository offers a dynamic simulation playground designed for training agents using Q-Learning algorithms. The environment is composed of particles that adhere to realistic physical behaviors, allowing for comprehensive training scenarios. The mechanics are highly flexible and scalable, enabling users to exercise control over the constituent elements to suit specific training goals.

![matrix](https://github.com/yago-mendoza/herding-sim/blob/main/ressources/matrix.gif)

## Execution

To engage with the simulation, Python and Pygame must be pre-installed on the local device. After installation, execute the file named `boid_modeling.py`. The user controls a dog that can be maneuvered via the mouse or arrow keys to herd the particles in the environment. The game is intended to serve as a testing ground for training agents using Q-Learning algorithms. To achieve this purpose, additional architectures can be programmed to control the dog's behavior in pursuit of specific training objectives.

### Simulation parameters
* `num_sheep`: number of sheep in the simulation.
* `spawn_radius`: the radius of the circle in which the sheep are spawned.
* `spawn_width`: the width of the circle in which the sheep are spawned.
* `spawn_top_speed`: the maximum speed that a sheep can have when spawned.
* `max_sheep_speed`: the maximum speed that a sheep can have.
* `dog_x, dog_y`: the initial position of the dog.
* `dog_speed`: the speed of the dog.
* `sheep_attraction_range`: the range within which the sheep are attracted to each other.
* `dog_repulsion_range`: the range within which the sheep are repelled by the dog.
* `wall_repulsion_factor`: the factor by which the sheep are repelled by the walls of the screen.
* `sheep_repulsion_factor`: the factor by which the sheep are repelled by each other.
* `dog_repulsion_factor`: the factor by which the sheep are repelled by the dog.

### Controls
* `ESC` to quit the game
* `a` to draw accelerations
* `v` to draw velocities
* `d` to draw the dog's repulsion range
* `c` to draw the clusters of sheep
* `k` to draw the indexes of sheep
* `s` to display clusters' statistics

## Code

The program's code structure consists of a series of flow structures and Pygame functions. Pygame is declared as a global variable and used throughout the code. The program begins by initializing Pygame and setting up the display window. Next, the program sets up the simulation environment and creates the boid particles, assigning each particle its unique characteristics. The simulation itself is run within a while loop that continuously updates the positions and behaviors of the particles. The loop also checks for user input and updates the display accordingly. Additionally, the program includes several functions for calculating various aspects of the boid particles' behavior. 

![test](https://github.com/yago-mendoza/herding-sim/blob/main/ressources/test.gif)

