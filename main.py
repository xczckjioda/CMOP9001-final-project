import pygame
from block import Block, bricks_layout_0, bricks_layout_0, bricks_layout_1,bricks_layout_2,bricks_layout_3,bricks_layout_4,bricks_layout_5,bricks_layout_6, colors_for_bricks
from globals import *
import random
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode(((field_width + 8) * brick_width, field_height * brick_height), 0, 32)
pygame.display.set_caption('Tetris')
game_over_img = pygame.image.load("resources/images/game_over.jpg")
font = pygame.font.Font("resources/fonts/MONACO.TTF", 18)

img_width = game_over_img.get_width()
img_height = game_over_img.get_height()
screen_width = screen.get_width()
screen_height = screen.get_height()

# Draw all the bricks that are currently placed on the field
def drawField():
    for brick in field_bricks:
        brick.draw(screen)

# Draws the score and preview of the next block on the side
def drawInfoPanel(next_block):
    text = font.render('score: ' + str(score[0]), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.topleft = ((field_width + 2) * brick_width + 15 , 40)
    screen.blit(text, textRect)
    next_block.draw(screen)

    title = font.render("next block", True, (0, 0, 0))
    screen.blit(title, ((field_width + 2) * brick_width, 200))

# Draws the "Pause" button and returns area for click detection
def drawPauseButton():
    button_color = (180, 180, 180)
    button_rect = pygame.Rect((field_width + 2) * brick_width, 100, 120, 40)
    pygame.draw.rect(screen, button_color, button_rect)
    text = font.render("Pause", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Draws the line separating the main field and the side panel
def drawFrame():
    pygame.draw.line(screen, pygame.Color(200, 200, 200),
                     (field_width * brick_width, 0),
                     (field_width * brick_width, field_height * brick_height), 3)


# Randomly generates a new block with a random shape and orientation
def getBlock():
    block_type = random.randint(0, 6)
    if block_type == 0:
        return Block(bricks_layout_0, random.randint(0, len(bricks_layout_0) - 1), colors_for_bricks[0])
    elif block_type == 1:
        return Block(bricks_layout_1, random.randint(0, len(bricks_layout_1) - 1), colors_for_bricks[1])
    elif block_type == 2:
        return Block(bricks_layout_2, random.randint(0, len(bricks_layout_2) - 1), colors_for_bricks[2])
    elif block_type == 3:
        return Block(bricks_layout_3, random.randint(0, len(bricks_layout_3) - 1), colors_for_bricks[3])
    elif block_type == 4:
        return Block(bricks_layout_4, random.randint(0, len(bricks_layout_4) - 1), colors_for_bricks[4])
    elif block_type == 5:
        return Block(bricks_layout_5, random.randint(0, len(bricks_layout_5) - 1), colors_for_bricks[5])
    elif block_type == 6:
        return Block(bricks_layout_6, random.randint(0, len(bricks_layout_6) - 1), colors_for_bricks[6])

# Saves the current game score to a file named scores.txt
def save_score(score_value):
    with open("scores.txt", "a") as f:
        f.write(str(score_value) + "\n")

# Appends a log entry of the game result with timestamp to log.txt
def log_game_result(score_value):
    with open("log.txt", "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] Game Over - Score: {score_value}\n")

# Displays the top 5 highest scores from scores.txt on the game over screen
def draw_leaderboard():
    try:
        with open("scores.txt", "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
        scores.sort(reverse=True)
        top_scores = scores[:5]

        title = font.render("Leaderboard", True, (0, 0, 0))
        screen.blit(title, (screen_width // 2 - 60, screen_height // 2-60))

        for i, s in enumerate(top_scores):
            line = font.render(f"{i+1}. {s}", True, (0, 0, 0))
            screen.blit(line, (screen_width // 2 - 60, screen_height // 2 - 30  + i * 25))
    except Exception as e:
        print("Error loading leaderboard:", e)

# Draws the "Restart" button on the game over screen and returns its rectangle for click detection
def draw_restart_button():
    button_font = pygame.font.SysFont("Arial", 24)
    button_color = (180, 180, 180)
    button_rect = pygame.Rect(screen_width // 2 - 60, screen_height // 2 + 120, 120, 40)
    pygame.draw.rect(screen, button_color, button_rect)
    text = button_font.render("Restart", True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect



def main():
    running = True
    next_block = None
    paused = False
    while running:
        cur_block = getBlock() if next_block is None else next_block
        cur_block.setPosition((4, 0))
        next_block = getBlock()
        next_block.setPosition((field_width + 3, 9))

        # Check if the starting position is blocked => Game Over
        if not cur_block.isLegal(cur_block.cur_layout, cur_block.position):
            cur_block.draw(screen)
            running = False
            break

        # Block falling loop
        while not cur_block.stopped:
            screen.fill((255, 255, 255))
            drawFrame()
            if not paused:
                cur_block.update(pygame.time.get_ticks(), screen)

            drawField()
            pause_button_rect = drawPauseButton()
            drawInfoPanel(next_block)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        continue
                    if not paused:
                        if event.key in [pygame.K_w, pygame.K_UP]:
                            cur_block.rotate()
                            last_move[0] = pygame.time.get_ticks()
                        elif event.key in [pygame.K_a, pygame.K_LEFT]:
                            cur_block.left()
                        elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                            cur_block.right()
                        elif event.key in [pygame.K_s, pygame.K_DOWN]:
                            cur_block.down()
                            last_move[0] = pygame.time.get_ticks() - 500
                    else:
                            print("Ignored key:", event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button_rect.collidepoint(event.pos):
                        paused = not paused

    # Game over actions: log result, display leaderboard and restart option
    log_game_result(score[0])
    save_score(score[0])
    screen.blit(game_over_img, ((screen_width - img_width) // 2, screen_height // 3 - img_height // 2-60 ))
    draw_leaderboard()
    restart_button = draw_restart_button()
    pygame.display.update()

    # Wait for user to click "Restart" or close window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):

                    field_map[:] = [[0 for _ in range(field_width)] for _ in range(field_height)]
                    field_bricks.clear()
                    score[0] = 0
                    last_move[0] = -1
                    main()
                    return
        pygame.display.update()

if __name__ == '__main__':
    main()