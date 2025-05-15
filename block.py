import random
import pygame
from brick import Brick

# size of each brick
brick_width = 30
brick_height = 30

# Width and height of the game field
field_width, field_height = 12, 17

#initial position of the block
cur_block_init_position = (4, 0)


# class of blocks
class Block:
    # constructor function of the block
    def __init__(self, p_bricks_layout, p_direction, p_color, position=cur_block_init_position):
        from globals import field_map  # delayed import to avoid circular import
        self.bricks_layout = p_bricks_layout
        self.direction = p_direction
        self.cur_layout = self.bricks_layout[self.direction]
        self.position = position
        self.stopped = False
        self.move_interval = 800
        self.bricks = [Brick((self.position[0] + x, self.position[1] + y), p_color)
                       for (x, y) in self.cur_layout]

    def setPosition(self, position):
        self.position = position
        self.refresh_bircks()

    #draw the block by the methods of the bricks
    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)

    def isLegal(self, layout, position):
        from globals import field_map
        (x0, y0) = position
        for (x, y) in layout:
            if x + x0 < 0 or y + y0 < 0 or x + x0 >= field_width or y + y0 >= field_height:
                return False
            if field_map[y + y0][x + x0] != 0:
                return False
        return True

    def left(self):
        new_position = (self.position[0] - 1, self.position[1])
        if self.isLegal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bircks()

    def right(self):
        new_position = (self.position[0] + 1, self.position[1])
        if self.isLegal(self.cur_layout, new_position):
            self.position = new_position
            self.refresh_bircks()

    def down(self):
        (x, y) = (self.position[0], self.position[1] + 1)
        while self.isLegal(self.cur_layout, (x, y)):
            self.position = (x, y)
            self.refresh_bircks()
            y += 1

    def refresh_bircks(self):
        for (brick, (x, y)) in zip(self.bricks, self.cur_layout):
            brick.position = (self.position[0] + x, self.position[1] + y)

    def stop(self):
        from globals import field_bricks, field_map, score, field_width
        self.stopped = True
        ys = []
        # Add the current block's bricks to the fixed field and update the map
        for brick in self.bricks:
            field_bricks.append(brick)
            (x, y) = brick.position
            if y not in ys:
                ys.append(y)
            field_map[y][x] = 1

        eliminate_count = 0
        ys.sort()

        # Check for full lines and eliminate them
        for y in ys:
            if 0 in field_map[y]:
                continue
            eliminate_count += 1
            # Move all lines above down by one
            for fy in range(y, 0, -1):
                field_map[fy] = field_map[fy - 1][:]
            field_map[0] = [0 for _ in range(field_width)]

            # Update brick positions
            tmp_field_bricks = []
            for fb in field_bricks:
                (fx, fy) = fb.position
                if fy < y:
                    fb.position = (fx, fy + 1)
                    tmp_field_bricks.append(fb)
                elif fy > y:
                    tmp_field_bricks.append(fb)
            field_bricks[:] = tmp_field_bricks
            # Update score based on number of lines eliminated
        score[0] += [0, 1, 2, 4, 6][eliminate_count]

    #falls automatically
    def update(self, time,screen):
        from globals import last_move
        self.draw(screen)
        if last_move[0] == -1 or time - last_move[0] >= self.move_interval:
            new_position = (self.position[0], self.position[1] + 1)
            if self.isLegal(self.cur_layout, new_position):
                self.position = new_position
                self.refresh_bircks()
                last_move[0] = time
            else:
                self.stop()

    def rotate(self):
        new_direction = (self.direction + 1) % len(self.bricks_layout)
        new_layout = self.bricks_layout[new_direction]
        if self.isLegal(new_layout, self.position):
            self.direction = new_direction
            self.cur_layout = new_layout
            self.refresh_bircks()

#the 7 kinds of layout of the bricks
bricks_layout_0 = (
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 1), (1, 1), (2, 1), (3, 1)))
bricks_layout_1 = (
        ((1, 0), (2, 0), (1, 1), (2, 1)),
        )
bricks_layout_2 = (
        ((1, 0), (0, 1), (1, 1), (2, 1)),
        ((0, 1), (1, 0), (1, 1), (1, 2)),
        ((1, 2), (0, 1), (1, 1), (2, 1)),
        ((2, 1), (1, 0), (1, 1), (1, 2)),
        )
bricks_layout_3 = (
        ((0, 1), (1, 1), (1, 0), (2, 0)),
        ((0, 0), (0, 1), (1, 1), (1, 2)),
        )
bricks_layout_4 = (
        ((0, 0), (1, 0), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (0, 1), (0, 2)),
        )
bricks_layout_5 = (
        ((0, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 2), (0, 1), (1, 1), (2, 1)),
        ((1, 0), (1, 1), (1, 2), (2, 2)),
        ((2, 0), (2, 1), (1, 1), (0, 1)),
        )
bricks_layout_6 = (
        ((2, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (1, 1), (1, 0)),
        ((2, 2), (2, 1), (1, 1), (0, 1)),
        )

#the colors of the bricks
colors_for_bricks = (
    pygame.Color(201, 117, 176), pygame.Color(128, 171, 190), pygame.Color(179, 183, 212),
    pygame.Color(123, 77, 123), pygame.Color(193, 186, 217), pygame.Color(0, 0, 0),
    pygame.Color(209, 195, 129)
)
