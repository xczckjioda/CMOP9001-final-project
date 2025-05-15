#define the global variables

# Width and height of the game field
field_width, field_height = 12, 17
# Width and height of each brick
brick_width, brick_height = 30, 30
# 2D array representing the current field (0 = empty, 1 = occupied)
field_map = [[0 for _ in range(field_width)] for _ in range(field_height)]
# List storing all landed  bricks on the field
field_bricks = []
#game score
score = [0]
# Time tick of last block move (wrapped in a list for mutability)
last_move = [-1]