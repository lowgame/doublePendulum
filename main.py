import pygame
import numpy as np

# Pygame
pygame.init()

# Screen Settings
width, height = 360, 640
screen = pygame.display.set_mode((width, height))

# Push Q for end the simulation.

# Pendulum Settings
length1 = 50 # first
length2 = 150 # second
mass1 = 1
mass2 = 1
# Initial Positions
angle1 = np.pi * 1.2
angle2 = np.pi / 3

angular_velocity1 = 0
angular_velocity2 = 0
gravity = 1

# Time step - Like FPS
dt = 0.2

# Pygame Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # EQUATIONS OF MOTION

    # Calculating accelerations...
    numerator1 = -gravity * (2 * mass1 + mass2) * np.sin(angle1)
    numerator2 = -mass2 * gravity * np.sin(angle1 - 2 * angle2)
    numerator3 = -2 * np.sin(angle1 - angle2) * mass2
    numerator4 = angular_velocity2**2 * length2 + angular_velocity1**2 * length1 * np.cos(angle1 - angle2)
    denominator = length1 * (2 * mass1 + mass2 - mass2 * np.cos(2 * angle1 - 2 * angle2))
    angular_acceleration1 = (numerator1 + numerator2 + numerator3 * numerator4) / denominator

    numerator1 = 2 * np.sin(angle1 - angle2)
    numerator2 = angular_velocity1**2 * length1 * (mass1 + mass2)
    numerator3 = gravity * (mass1 + mass2) * np.cos(angle1)
    numerator4 = angular_velocity2**2 * length2 * mass2 * np.cos(angle1 - angle2)
    denominator = length2 * (2 * mass1 + mass2 - mass2 * np.cos(2 * angle1 - 2 * angle2))
    angular_acceleration2 = (numerator1 * (numerator2 + numerator3 + numerator4)) / denominator

    # Changings the velocities and angles...
    angular_velocity1 += angular_acceleration1 * dt
    angular_velocity2 += angular_acceleration2 * dt
    angle1 += angular_velocity1 * dt
    angle2 += angular_velocity2 * dt

    # Calculating the mod of the angle, to avoid "big number" errors.
    angle1 = angle1 % (2 * np.pi)
    angle2 = angle2 % (2 * np.pi)

    # Calculating balls positions
    x1 = length1 * np.sin(angle1)
    y1 = length1 * np.cos(angle1)
    x2 = x1 + length2 * np.sin(angle2)
    y2 = y1 + length2 * np.cos(angle2)

    # Drawing the lines and balls.
    pygame.draw.line(screen, (0, 0, 0), (width/2, height/2), (width/2 + x1, height/2 + y1))
    pygame.draw.circle(screen, (0, 0, 255), ((width/2 + x1), (height/2 + y1)), 10)
    pygame.draw.line(screen, (0, 0, 0), (width/2 + x1, height/2 + y1), (width/2 + x2, height/2 + y2))
    pygame.draw.circle(screen, (0, 0, 255), ((width/2 + x2), (height/2 + y2)), 10)

    # Update the display
    pygame.display.flip()

    # Like - FPS
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()