import math
from collections import deque

import numpy as np
import pygame
from numpy import random

from background import get_grid

# Initialize Pygame and its screen
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 18)
running=True
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
background = get_grid(SCREEN_WIDTH,SCREEN_HEIGHT)

FPS=15
t_s=1/FPS

# +++++++++++++++++++++++++++++++++++++++++++++++
#   SECTION 1 : SETUP PARAMETERS
# +++++++++++++++++++++++++++++++++++++++++++++++

# =========== SIMULATIONS PARAMETERS ============

# Initial conditions
num_sheep = 200
spawn_radius = 350
spawn_top_speed = 100
max_sheep_speed = 50
dog_x, dog_y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
dog_speed = 10

# Attraction and repulsion factors and ranges
sheep_attraction_range = 150
dog_repulsion_range = 150
wall_repulsion_factor = 0 # 20
sheep_repulsion_factor = 500 # 500
dog_repulsion_factor = 5000 # 10000

# Interface preferences
draw_dog_repulsion_range = True
dog_repulsion_range_color = (255, 0, 0, 15)
draw_acceleration = True
draw_velocity = True
draw_sheep_index = True
draw_cluster_stats = True
draw_clusters = True
clusters_color = (255, 255, 255)

# =========== INITIALISING VARIABLES ============

# Sheeps are represented by these 6 vectors
p_x, p_y = np.zeros(num_sheep), np.zeros(num_sheep)
v_x, v_y = np.zeros(num_sheep), np.zeros(num_sheep)
a_x, a_y = np.zeros(num_sheep), np.zeros(num_sheep)

for k in range(num_sheep):
    # We arrange the sheeps in a circle and assign them random speeds 
    p_x[k] = SCREEN_WIDTH/2 + spawn_radius*math.cos(k)
    p_y[k] = SCREEN_HEIGHT/2 + spawn_radius*math.sin(k)
    v_x[k] = (random.rand()*spawn_top_speed*2)-(spawn_top_speed) # [-100,100]
    v_y[k] = (random.rand()*spawn_top_speed*2)-(spawn_top_speed) # [-100,100]

dist = np.zeros(num_sheep) # distance between a sheep and all others (reused)

# +++++++++++++++++++++++++++++++++++++++++++++++
#   SECTION 2 : SIMULATION
# +++++++++++++++++++++++++++++++++++++++++++++++

while running:

    # ============= USER INPUT HANDLING =============
    
    # KEYWORD-INPUT HANDLING
    for event in pygame.event.get():
        # Window close-button
        if event.type == pygame.QUIT:
            running=False
        # "ESC" to quit the game
        # "a" to draw accelerations
        # "v" to draw velocities
        # "d" to draw the dog's repulsion range
        # "c" to draw the clusters of sheep
        # "k" to draw the indexes of sheep
        # "s" to display clusters' statistics
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                draw_acceleration = not draw_acceleration
            elif event.key == pygame.K_v:
                draw_velocity = not draw_velocity
            elif event.key == pygame.K_d:
                draw_dog_repulsion_range = not draw_dog_repulsion_range
            elif event.key == pygame.K_k:
                draw_sheep_index = not draw_sheep_index
            elif event.key == pygame.K_c:
                draw_clusters = not draw_clusters
            elif event.key == pygame.K_s:
                draw_cluster_stats = not draw_cluster_stats
                if not draw_clusters:
                    draw_cluster_stats = False
            elif event.key == pygame.K_ESCAPE:
                running = False

    # CONTINUOUS PRESSES
    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_LEFT]:
        if dog_x > 0:
            dog_x -= dog_speed
    if key_input[pygame.K_UP]:
        if dog_y > 0:
            dog_y -= dog_speed
    if key_input[pygame.K_RIGHT]:
        if dog_x < 1920:
            dog_x += dog_speed
    if key_input[pygame.K_DOWN]:
        if dog_y < 1080:
            dog_y += dog_speed

    # MOUSE-INPUT
    if pygame.mouse.get_pressed()[0]: # left
        mouse_pos = pygame.mouse.get_pos()
        dog_x, dog_y = mouse_pos
    elif pygame.mouse.get_pressed()[2]: # right
        mouse_pos = pygame.mouse.get_pos()
        center_of_mass_x = np.average(p_x, weights=np.ones(num_sheep))
        center_of_mass_y = np.average(p_y, weights=np.ones(num_sheep))
        delta_x, delta_y = mouse_pos[0] - center_of_mass_x, mouse_pos[1] - center_of_mass_y
        p_x += delta_x
        p_y += delta_y

    # ========= ELEMENTS DISPLAY =========

    # 1. GRID
    screen.blit(background, (0,0))
   
    # 2. DOG
    pygame.draw.circle(screen, (255,0,0), (dog_x, dog_y), 10) # the dog itself
    if draw_dog_repulsion_range:
        # Layer for the circle's transparent fill
        dog_repulsion_range_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA) 
        pygame.draw.circle(dog_repulsion_range_surface, dog_repulsion_range_color, (int(dog_x), int(dog_y)), dog_repulsion_range, 0)
        screen.blit(dog_repulsion_range_surface, (0, 0))
        # Contour of the circle
        pygame.draw.circle(screen, (255,0,0), (dog_x, dog_y), dog_repulsion_range, 1)
    
    # 3. SHEEP
    for k in range(num_sheep):
        # Iterating through each sheep by its index

        # Initializing acceleration components for each sheep
        a_wall_x, a_wall_y = 0, 0
        a_center_x, a_center_y = 0, 0
        a_static_x, a_static_y = 0, 0
        a_dog_x, a_dog_y = 0, 0

        # ===== SHEEP ACCELERATION COMPONENTS =====
        
        # 1. Acceleration component due to terrain friction

        a_friction_x = v_x[k]*(-1)
        a_friction_y = v_y[k]*(-1)

        # 2. Acceleration component due to sheep attraction
        
        for j in range(num_sheep):
            # Calculate the distance between the current sheep and all other sheep
            dist[j]=math.hypot(p_x[j] - p_x[k], p_y[j] - p_y[k])
        # Calculate the average X and Y positions for the nearby sheep
        center_x = np.mean(p_x[dist<=sheep_attraction_range])
        center_y = np.mean(p_y[dist<=sheep_attraction_range])
        # Find the distance between the current sheep and the center
        sheep_dist_center_x = (center_x-p_x[k]) 
        sheep_dist_center_y = (center_y-p_y[k])

        a_center_x = sheep_dist_center_x 
        a_center_y = sheep_dist_center_y

        # 3. Acceleration component due to sheep repulsion

        closest_sheep = np.where(dist==np.min(dist[dist!=0]))[0].item() # sometimes Error
        # Finds the index 'k' sheep of the closest sheep (closest_sheep)
        closest_sheep_dist = dist[closest_sheep]
        if (closest_sheep_dist<sheep_attraction_range):
            ang=math.atan((p_y[k]-p_y[closest_sheep])/(p_x[closest_sheep]-p_x[k])) # angle(line(sheep,sheep),x_axis)
            a_static_x=(1/closest_sheep_dist)*np.cos(ang)*(np.abs(p_x[k]-p_x[closest_sheep])/(p_x[k]-p_x[closest_sheep]))*sheep_repulsion_factor
            a_static_y=(1/closest_sheep_dist)*np.sin(ang)*sheep_repulsion_factor*(-1 if a_static_x > 0 else 1)

        # 4. Acceleration component due to dog

        sheep_dog_distance = math.hypot(dog_x-p_x[k], dog_y - p_y[k])
        if (sheep_dog_distance<dog_repulsion_range):
            ang=math.atan((p_y[k]-dog_y)/(dog_x-p_x[k])) # angle(line(sheep,dog),x_axis)
            a_dog_x=(1/sheep_dog_distance)*np.cos(ang)*(np.abs(p_x[k]-dog_x)/(p_x[k]-dog_x))*dog_repulsion_factor
            a_dog_y=(1/sheep_dog_distance)*np.sin(ang)*dog_repulsion_factor*(-1 if a_dog_x > 0 else 1)

        # 5. Acceleration component due to wall (+check margin violations)
        safety_margin = 200
        top_margin, bottom_margin = safety_margin, SCREEN_HEIGHT-safety_margin
        left_margin, right_margin = safety_margin, SCREEN_WIDTH-safety_margin
        if (p_x[k]<=left_margin):
            a_wall_x=(left_margin-p_x[k])*wall_repulsion_factor
            if (p_x[k]<0):
                p_x[k]=0
                v_x[k]=v_x[k]*-1
        elif (p_x[k]>right_margin):
            a_wall_x=(right_margin-p_x[k])*wall_repulsion_factor
            if (p_x[k]>SCREEN_WIDTH):
                p_x[k]=SCREEN_WIDTH
                v_x[k]=v_x[k]*-1
        elif (p_y[k]<=top_margin):
            a_wall_y=(right_margin-p_y[k])*wall_repulsion_factor
            if (p_y[k]<0):
                p_y[k]=0
                v_y[k]=v_y[k]*-1
        elif (p_y[k]>bottom_margin):
            a_wall_y=(bottom_margin-p_y[k])*wall_repulsion_factor
            if (p_y[k]>SCREEN_HEIGHT):
                p_y[k]=SCREEN_HEIGHT
                v_y[k]=v_y[k]*-1

        # Update kinematic vectors (obeying MRUA equations)

        a_x[k] = a_friction_x + a_center_x + a_static_x + a_dog_x + a_wall_x
        a_y[k] = a_friction_y + a_center_y + a_static_y + a_dog_y + a_wall_y

        v_x[k] = v_x[k] + a_x[k]*t_s
        v_y[k] = v_y[k] + a_y[k]*t_s

        v_x[k] = min(v_x[k], max_sheep_speed) # check speed limit violations
        v_y[k] = min(v_y[k], max_sheep_speed) # check speed limit violations

        p_x[k] = p_x[k] + v_x[k]*t_s + 0.5*a_x[k]*t_s**2
        p_y[k] = p_y[k] + v_y[k]*t_s + 0.5*a_y[k]*t_s**2

        # ===== DRAW =====

        # Draws the sheep
        pygame.draw.circle(screen, (255,255,255), (p_x[k], p_y[k]), 3)

        # Draw sheep index
        if draw_sheep_index:
            text = font.render(str(k), True, (255, 255, 255))
            screen.blit(text, (p_x[k] + 5, p_y[k] + 5))

        # Draws other geometry        
        if draw_acceleration:
            pygame.draw.line(screen, (255,0,0), (p_x[k], p_y[k]), (p_x[k]+a_center_x, p_y[k]+a_center_y))
        if draw_velocity:
            pygame.draw.line(screen, (0,255,0), (p_x[k], p_y[k]), (p_x[k]-a_friction_x, p_y[k]-a_friction_y))

    # 4. GENERAL GEOMETRY

    if draw_clusters:

        # Get the clusters of sheep (lists of "k")
        clusters = [] # Initialize an empty list to store the clusters of sheep
        visited = set() # Initialize a set to keep track of visited sheep
        for i in range(num_sheep):
            if i not in visited:
                visited.add(i)
                cluster = [i] # Start a new cluster with the current sheep
                queue = deque([i]) # Initialize a queue with the current sheep to process its neighbors
                while queue:
                    # Process neighbors until the queue is empty
                    current_sheep = queue.popleft() # Remove the first sheep from the queue
                    for j in range(num_sheep): # Iterate through all the sheep
                        if j not in visited:
                            ds = math.hypot(p_x[j] - p_x[current_sheep], p_y[j] - p_y[current_sheep])
                            # Check if the distance is within the sheep_attraction_range
                            if ds <= sheep_attraction_range:
                                cluster.append(j) # Add the sheep to the current cluster
                                queue.append(j)  # Add the sheep to the queue to process its neighbors
                                visited.add(j) # Mark the sheep as visited
                clusters.append(cluster)
        # Obtained the "clusters" list.

        if draw_cluster_stats:

            q_mov_clusters = []
            # Computes the momentum of every cluster
            for cluster in clusters:
                q_mov = 0
                for sheep in cluster:
                    q_mov += abs(v_x[sheep])+abs(v_y[sheep])
                q_mov_clusters.append(q_mov/len(cluster))

    if draw_clusters:

        for i,cluster in enumerate(clusters):
            # We will only draw clusters containing more than one single sheep
            if len(cluster) > 1:

                # Draw the cluster's bounding box
                min_x = min(p_x[sheep] for sheep in cluster)
                min_y = min(p_y[sheep] for sheep in cluster)
                max_x = max(p_x[sheep] for sheep in cluster)
                max_y = max(p_y[sheep] for sheep in cluster)
                rect_width, rect_height = max_x - min_x, max_y - min_y
                pygame.draw.rect(screen, clusters_color, (min_x, min_y, rect_width, rect_height), 1)

                if draw_cluster_stats:

                    square_size = 8 # Draws a small white square at each corner
                    pygame.draw.rect(screen, (255, 255, 255), (min_x, min_y, square_size, square_size))
                    pygame.draw.rect(screen, (255, 255, 255), (max_x - square_size, min_y, square_size, square_size))
                    pygame.draw.rect(screen, (255, 255, 255), (min_x, max_y - square_size, square_size, square_size))
                    pygame.draw.rect(screen, (255, 255, 255), (max_x - square_size, max_y - square_size, square_size, square_size))
                    
                    # Draws the momentum bar
                    bar_width = rect_width * q_mov_clusters[i]/sum(q_mov_clusters)
                    bar_x, bar_y = min_x, max_y + 5
                    pygame.draw.rect(screen, clusters_color, (bar_x, bar_y, bar_width, 6), 0)
                    pygame.draw.rect(screen, clusters_color, (bar_x, bar_y, rect_width, 6), 1)

                    # Adds text showing percentage of sheep in the cluster
                    percentage = "{:.2%}".format(len(cluster)/num_sheep)
                    text = font.render(percentage, True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.midright = (max_x, min_y - 10)
                    screen.blit(text, text_rect)

    # Flip the display
    pygame.display.flip()