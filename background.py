import math

import numpy as np
import pygame


def get_grid (SCREEN_WIDTH, SCREEN_HEIGHT,
        rough_square_side_size = 100,
        minor_grid_scale_down = 5,
        colors = ((200,200,200),(60,60,60))
        ):
    
    # rough_square_side_size *= zoom_scale (if introduced "zoom_scale" argument)

    major_grid_n_cols = math.ceil(SCREEN_WIDTH / rough_square_side_size)
    major_grid_n_rows = math.ceil(SCREEN_HEIGHT / rough_square_side_size)
    
    major_grid_size_x = SCREEN_WIDTH / major_grid_n_cols
    minor_grid_size_x = major_grid_size_x / minor_grid_scale_down
    major_grid_size_y = SCREEN_HEIGHT / major_grid_n_rows
    minor_grid_size_y = major_grid_size_y / minor_grid_scale_down

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for x in np.arange(0, SCREEN_WIDTH, minor_grid_size_x):
        if abs(x % major_grid_size_x) > 0.00:
            pygame.draw.line(background, colors[1], (x, 0), (x, SCREEN_HEIGHT))
    for y in np.arange(0, SCREEN_HEIGHT, minor_grid_size_y):
        if abs(y % major_grid_size_y) > 0.00:
            pygame.draw.line(background, colors[1], (0, y), (SCREEN_WIDTH, y))
    for x in np.arange(0, SCREEN_WIDTH, major_grid_size_x):
        pygame.draw.line(background, colors[0], (x, 0), (x, SCREEN_HEIGHT))
    for y in np.arange(0, SCREEN_HEIGHT, major_grid_size_y):
        pygame.draw.line(background, colors[0], (0, y), (SCREEN_WIDTH, y))
    return background
    