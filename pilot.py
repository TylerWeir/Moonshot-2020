# This module will represent the pilot controlling a ship using Craig Reynold's
# flocking algorithim
import math
from vector2d import Vector2D


class Pilot():
    def __init__(self):
        self.max_acceleration = 0.1
        self.sightRange = 150

    # TODO: Scales request by 1/d
    def calc_avoid(self, boids, position):
        """Returns the avoid accerlation"""
        avoidAccel = Vector2D(0, 0)
        range = 30
        weight = 1/10

        # Add up all the separation vectors
        for boid in boids:
            if math.dist(position, boid.rect.center) < range:
                xdiff = position[0]-boid.rect.center[0]
                ydiff = position[1]-boid.rect.center[1]
                diff = Vector2D(xdiff, ydiff)
                diff.scale(1/(diff.calc_magnitude()))
                avoidAccel.add(diff)

        avoidAccel.scale(weight)
        return avoidAccel

    #
    def calc_align(self, boids, velocity):
        """Returns the acceleration vector to align velocity direction with the
        average velocity direction of nearby boids."""
        velocities = Vector2D(0, 0)
        weight = 1/16

        # No change if there are no other boids around.
        if not(len(boids)):
            return Vector2D(0, 0)

        # Accumulates velocities
        for boid in boids:
            velocities.add_values(boid.velocity.x, boid.velocity.y)

        # Averages velocities
        if len(boids) > 1:
            velocities.scale(1/(len(boids)-1))

        xdiff = velocities.x - velocity.x
        ydiff = velocities.y - velocity.y
        alignAccel = Vector2D(xdiff, ydiff)
        alignAccel.scale(weight)
        return alignAccel

    def calc_approach(self, boids, position):
        """Returns the approach accerlation"""
        approachAccel = Vector2D(0, 0)
        weight = 1/100

        # Add up all the separation vectors
        for boid in boids:
            xdiff = boid.rect.center[0]-position[0]
            ydiff = boid.rect.center[1]-position[1]
            approachAccel.add_values(xdiff, ydiff)

        # Makes accleration based on average position
        if len(boids) > 0:
            approachAccel.scale(1/len(boids))

        approachAccel.scale(weight)
        return approachAccel

    def get_acceleration(self, position, velocity, boids):
        """Returns a single acceleration vector in response to nearby boids."""

        # Find the neighboring boids
        neighbors = self.find_neighbors(boids, position, self.sightRange)

        # Acceleration acccumulator
        # Add acceleration requests in order of importance
        accelRequests = [
            self.calc_avoid(neighbors, position),
            self.calc_align(neighbors, velocity),
            self.calc_approach(neighbors, position)]

        # for request in accelRequests:
        # print(str(request))

        # print("")

        # Add up requests untill max acceleration is reached
        acceptedRequests = Vector2D(0, 0)
        for request in accelRequests:
            # Add if room
            if acceptedRequests.calc_magnitude() < self.max_acceleration:
                acceptedRequests.add(request)
            # Trim tail if over
            if acceptedRequests.calc_magnitude() > self.max_acceleration:
                excess = acceptedRequests.calc_magnitude()-self.max_acceleration
                request.normalize()
                request.scale(-excess)
                acceptedRequests.add(request)

        # print("Accepted Acceleration: " + str(acceptedRequests))
        # print(f"magnitude: {acceptedRequests.calc_magnitude()}")
        # print("")
        return acceptedRequests

    def find_neighbors(self, boids, position, distance):
        """Finds all the boids in a given list within the given distance of the
        indicated position."""

        # List to hold nearby boids
        nearbyBoids = []

        # Keep boids within distance
        for boid in boids:
            d = math.dist(position, boid.rect.center)
            if((d < distance) and (d > 0)):
                nearbyBoids.append(boid)

        return nearbyBoids
