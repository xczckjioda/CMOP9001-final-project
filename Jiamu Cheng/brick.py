import pygame

# size of each brick
brick_width = 30
brick_height = 30


# class of a single brick unit on the Tetris board.
class Brick:
    #constructor function of the brick
    def __init__(self, p_position, p_color):
        self.position = p_position
        self.color = p_color
        self.image = pygame.Surface([brick_width, brick_height])
        self.image.fill(self.color)
    #draw a brick on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.position[0] * brick_width, self.position[1] * brick_height))
