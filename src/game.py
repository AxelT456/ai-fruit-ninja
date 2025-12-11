import cv2
import numpy as np
import random

class Fruit:
    def __init__(self, screen_width=1280, screen_height=720):
        """
        Initializes a Fruit object with random position and type.
        """

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initial position: Lower part of the screen with random x-coordinate
        self.x = random.randint(100, screen_width - 100)
        self.y = screen_height + 50  # Start off-screen

        # Physics / Velocity
        self.speed_x = random.randint(-10,10)
        self.speed_y = random.randint(-35, -28) # Upward velocity
        self.gravity = 1 # Gravity effect

        # Appearance
        colors = [(0,255,0), (0,0,255), (0,165,255), (0,255,255)]
        self.color = random.choice(colors)
        self.radius = 60 # Size of the fruit

    def update(self):
        """
        Updates the fruit's position based on its velocity and gravity.
        Returns True if the fruit is still on screen, False otherwise.
        """

        self.x += self.speed_x # Move in x
        self.y += self.speed_y # Apply gravity to y-velocity
        self.speed_y += self.gravity

        if self.y > self.screen_height + 100:
            return False # Fruit is off-screen
        return True
    
    def draw(self, img):
        """
        Draws the fruit on the given image.
        """

        cv2.circle(img, (int(self.x), int(self.y)), self.radius, self.color, cv2.FILLED)