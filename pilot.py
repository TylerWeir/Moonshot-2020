# This module will represent the pilot controlling a ship using Craig Reynold's
# flocking algorithim
import math


class Pilot():
    def __init__(self):
        self.max_acceleration = 2
        self.avoid_distance = 20
        self.align_distance = 50
        self.approach_distance = 100

    def calc_avoid_acceleration(self, boids, position):
        """Returns the avoid accerlation"""
        # Tuple to accumulate the separation vectors
        separations = (0, 0)
        magnitude = 0

        # Catch the zero case
        if(len(boids) == 0):
            return (0, 0)

        # Add up all the separation vectors
        for boid in boids:
            separation = (position[0]-boid.rect.center[0],
                          position[1]-boid.rect.center[1])
            magnitude += self.vector_magnitude(separation)
            separation = self.scale_vector(separation, (1/self.vector_magnitude(separation))**2)
            separations = (separations[0] + separation[0],
                           separations[1] + separation[1])

        magnitude = magnitude/len(boids)
        magnitude = magnitude/5
        return self.scale_vector(self.normalize_vector(separations), 50/(magnitude**2))

    def calc_align_acceleration(self, boids):
        """Returns the acceleration vector to align velocity direction with the
        average velocity direction of nearby boids."""
        # Catch the zero case that sometimes arises
        if len(boids) == 0:
            return (0, 0)

        # Add up all the normalized velocity vectors and devide by n
        velocityAccumulator = (0, 0)
        for boid in boids:
            unitVelocity = self.normalize_vector(boid.velocity)
            velocityAccumulator = (velocityAccumulator[0] + unitVelocity[0],
                                   velocityAccumulator[1] + unitVelocity[1])
        return(self.scale_vector(velocityAccumulator, 1/len(boids)))

    def calc_approach_acceleration(self, boids, position):
        """Returns the approach accerlation"""
        # Tuple to accumulate the positions
        pos = (0, 0)

        for boid in boids:
            pos = (pos[0] + boid.rect.center[0],
                   pos[1] + boid.rect.center[1])

        avgPosition = 0
        if(len(boids) == 0):
            avgPosition = position
        else:
            avgPosition = (pos[0]/len(boids), pos[1]/len(boids))

        # print(f"The focus bird is at position: {position}")
        # print(f"The average position of nearby boids is: {avgPosition}")

        separation_vector = (avgPosition[0] - position[0], avgPosition[1] - position[1])
        return self.scale_vector(self.normalize_vector(separation_vector), 0.5)

    def get_acceleration(self, position, boids):
        """Returns a single acceleration vector in response to nearby boids."""
        # Needs to get the acceleration from each rule, then compose into
        # a single vector based on the weights of each rule.

        # Work from large range to small range to recycle the boid list

        # Approach Response
        nearbyBoids = self.find_nearby_boids(boids, position,
                                             self.approach_distance)
        approachAcceleration = self.calc_approach_acceleration(nearbyBoids, position)
        # print(f"The approach accerleration is {approachAcceleration}")

        # Align velocity Response
        nearbyBoids = self.find_nearby_boids(nearbyBoids, position, self.align_distance)
        alignAcceleration = self.calc_align_acceleration(nearbyBoids)
        # print(f"The align accerleration is {alignAcceleration}")

        # Avoid Response
        nearbyBoids = self.find_nearby_boids(nearbyBoids, position, self.avoid_distance)
        avoidAcceleration = self.calc_avoid_acceleration(nearbyBoids, position)

        # Return final condensed acceleration
        totalAccel = (approachAcceleration[0] + alignAcceleration[0] + avoidAcceleration[0],
                      approachAcceleration[1] + alignAcceleration[1] + avoidAcceleration[1])
        totalAccel = self.scale_vector(self.normalize_vector(totalAccel), 0.1)
        return totalAccel

    def find_nearby_boids(self, boids, position, distance):
        """Finds all the boids in a given list within the given distance of the
        indicated position."""

        # List to hold nearby boids
        nearbyBoids = []

        # print("")
        # print(f"Checking {len(boids)} for nearby boids")

        # Adds a boid to the return list if it is closer than distance
        for boid in boids:
            d = math.dist(position, boid.rect.center)
            if((d < distance) and (d > 0)):
                nearbyBoids.append(boid)
                # print(f"{math.dist(position, boid.rect.center)} is less than {distance}.")

        # print(f"Found {len(nearbyBoids)} nearby boids")
        return nearbyBoids

    def normalize_vector(self, vector):
        magnitude = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])

        if magnitude == 0:
            return vector
        else:
            return(vector[0]/magnitude, vector[1]/magnitude)

    def scale_vector(self, vector, scale):
        return (vector[0]*scale, vector[1]*scale)

    def vector_magnitude(self, vector):
        return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
