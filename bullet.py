# This class represnts a bullet shot into space.
import pygame
from vector2d import Vector2D

# Create a surface that will represent a bullet
bulletSurf = pygame.Surface((5, 2))
bulletSurf.fill((255, 255, 255))

# set a color key for blitting
bulletSurf.set_colorkey((255, 0, 0))
laser = pygame.Rect(0, 0, 5, 2)
pygame.draw.rect(bulletSurf, (0, 255, 0), laser)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, velocity, position):
        # Initialize the super sprite class
        super(Bullet, self).__init__()

        # Give a velocity in same direction as the ship with specified speed.
        self.speed = 12
        self.velocity = Vector2D(velocity[0], velocity[1])
        self.velocity.normalize()
        self.velocity.scale(self.speed)

        # Take the default surface and set to initial position.
        self.surf = bulletSurf
        self.rect = self.surf.get_rect(center=position)
        self.rotate(self.velocity.calc_angle())

        # Lifespan of the bullet in frames
        self.lifespan = 120

    # Update function to move the bullet through space
    def update(self):
        # Move by the velocity
        self.rect.move_ip(self.velocity.to_tuple())

        # Loops the edges of the screen
        if(self.rect.right < 0):
            self.rect.left = 800
        if(self.rect.left > 800):
            self.rect.right = 0
        if(self.rect.top > 800):
            self.rect.bottom = 0
        if(self.rect.bottom < 0):
            self.rect.top = 800

        # Kill the bullet if the lifespan is zero, otherwise, decrement it by
        # one frame
        if self.lifespan <= 0:
            self.kill()
        else:
            self.lifespan -= 1

    def rotate(self, angle):
        # save the old center postion
        oldCenter = self.rect.center

        # sets the current surface to the enemy surface rotated to the
        # indicated angle
        self.surf = pygame.transform.rotate(bulletSurf, angle)

        # get the rect of the rotated surf and set it's center to the saved
        self.rect = self.surf.get_rect()
        self.rect.center = oldCenter
