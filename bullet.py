import pygame
import math

# Create a surface that will represent a bullet
bulletSurf = pygame.Surface((2, 2))
bulletSurf.fill((255, 255, 255))

# Set a color key for blitting
bulletSurf.set_colorkey((255, 0, 0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, velocity, position):
        # initialize the super sprite class
        super(Bullet, self).__init__()

        # Give a velocity in same direction as the ship
        # Double the speed
        self.speed = 6
        self.velocity = self.normalize_vector(velocity)
        self.velocity = self.scale_vector(self.velocity, self.speed)

        # Face direction of velocity if there is length

        # Give surface
        self.surf = bulletSurf
        self.rect = self.surf.get_rect(center=position)

        self.lifespan = 120

    def update(self):
        # Move by the velocity
        self.rect.move_ip(self.velocity)

        # Loopscreen
        if(self.rect.right < 0):
            self.rect.left = 800
        if(self.rect.left > 800):
            self.rect.right = 0
        if(self.rect.top > 800):
            self.rect.bottom = 0
        if(self.rect.bottom < 0):
            self.rect.top = 800

        # Kill if been around for all frames in lifespan (60fps)
        if self.lifespan < 0:
            self.kill()
        else:
            self.lifespan -= 1

    def calc_rotation(self, v):
        newtheta = math.atan2(v[1], v[0])
        return 180-math.degrees(newtheta)

    def normalize_vector(self, vector):
        magnitude = self.vector_magnitude(vector)

        if magnitude == 0:
            return vector
        else:
            return(vector[0]/magnitude, vector[1]/magnitude)

    def scale_vector(self, vector, scale):
        return (vector[0]*scale, vector[1]*scale)

    def vector_magnitude(self, vector):
        return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])