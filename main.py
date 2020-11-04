"""This program is my submission to the 2020 Game Off hosted by itch.io"""

# Imports the pygame module
import pygame
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN
)

pygame.init()

screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

running = True
# Game loop
while running:

    # Quit if the user presses the close button.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Was a key pressed?
        elif event.type == KEYDOWN:
            # Quit if the escape key is pressed.
            if event.key == K_ESCAPE:
                running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()
