#September 2021
#Simple Flappy Bird game copy. I never got to play it when it was available in the app stores so I created something similar to recreate the apparently frustrating experience the game elicited

import pygame
import random
import sys
import pygame.mask
import numpy as np

# Set up the game window
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
pygame.init()
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load game assets
bird_img = pygame.image.load("bird.png")
pipe_img = pygame.image.load("pipe.png")
background_img = pygame.image.load("background.png")
# Scale the background image to fit the game window
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Define game variables
bird_x = 50
bird_y = 200
bird_velocity = 0
gravity = 0.5
jump_strength = 10
pipe_gap = 150
pipe_width = 50
pipe_height = 320
pipe_spacing = 150
pipe_list = []
score = 0
font = pygame.font.Font(None, 50)

# Define dynamic font size based on window height
font_size = int(WINDOW_HEIGHT * 0.05)
font = pygame.font.Font(None, font_size)

# Game states
HOME = 0
PLAYING = 1
game_state = HOME  # Start at the home page

# Define game functions
def draw_bird():
    game_display.blit(bird_img, (bird_x, bird_y))

def draw_pipes():
    for pipe in pipe_list:
        top_pipe_y = pipe["top"] - pipe_img.get_height()
        bottom_pipe_y = pipe["bottom"]
        game_display.blit(pygame.transform.flip(pipe_img, False, True), (pipe["x"], top_pipe_y))
        game_display.blit(pipe_img, (pipe["x"], bottom_pipe_y))



def move_pipes():
    for pipe in pipe_list:
        pipe["x"] -= 3
    if pipe_list and pipe_list[0]["x"] < -pipe_width:
        pipe_list.pop(0)

def add_pipe():
    global pipe_list, pipe_gap, pipe_spacing
    if len(pipe_list) < 5:
        max_gap_pos = WINDOW_HEIGHT - pipe_gap
        random_gap_pos = random.randint(pipe_gap, max_gap_pos)
        random_next_gap = random_gap_pos + 100  # Randomize the gap between the current and next pipe
        if not pipe_list:
            # Add the first pipe
            pipe_list.append({"x": WINDOW_WIDTH, "top": random_gap_pos - pipe_gap // 2, "bottom": random_gap_pos + pipe_gap // 2, "scored": False})
        else:
            # Add subsequent pipes after the last one
            last_pipe = pipe_list[-1]
            pipe_list.append({"x": last_pipe["x"] + pipe_spacing, "top": random_next_gap - pipe_gap // 2, "bottom": random_next_gap + pipe_gap // 2, "scored": False})

        # Randomize the gap between 150 and 250
        pipe_gap = random.randint(100, 250)

            

        
def get_visible_pipe_mask(pipe_rect):
    # Get the mask for the visible part of the pipe
    pipe_surface = pygame.Surface((pipe_width, pipe_gap))
    pipe_surface.blit(pipe_img, (0, 0), (0, pipe_img.get_height() - pipe_gap, pipe_width, pipe_gap))
    return pygame.mask.from_surface(pipe_surface)

def check_collision():
    bird_rect = bird_img.get_rect(topleft=(bird_x, bird_y))
    bird_collision_rect = pygame.Rect(bird_x + 7, bird_y + 7, bird_img.get_width() - 14, bird_img.get_height() - 14)

    for pipe in pipe_list:
        top_pipe_rect = pipe_img.get_rect(midbottom=(pipe["x"], pipe["top"]))
        bottom_pipe_rect = pipe_img.get_rect(midtop=(pipe["x"], pipe["bottom"]))

        # Create collision rectangles for the visible parts of the pipes, including the tips
        top_pipe_collision_rect = pygame.Rect(pipe["x"], 0, pipe_width, pipe["top"] - pipe_gap // 2)
        bottom_pipe_collision_rect = pygame.Rect(pipe["x"], pipe["bottom"] + pipe_gap // 2, pipe_width, WINDOW_HEIGHT - pipe["bottom"] - pipe_gap // 2)

        # Create collision rectangles for the tips of the pipes
        top_pipe_tip_collision_rect = pygame.Rect(pipe["x"], pipe["top"] - pipe_img.get_height(), pipe_width, pipe_img.get_height())
        bottom_pipe_tip_collision_rect = pygame.Rect(pipe["x"], pipe["bottom"], pipe_width, pipe_img.get_height())

        # Combine the rectangles for the visible parts and the tips
        top_pipe_collision_rect = top_pipe_collision_rect.union(top_pipe_tip_collision_rect)
        bottom_pipe_collision_rect = bottom_pipe_collision_rect.union(bottom_pipe_tip_collision_rect)

        # Reduce the tolerance for the left, right, top, and bottom sides of the collision rectangles
        top_pipe_collision_rect.left += 5
        top_pipe_collision_rect.right -= 5
        top_pipe_collision_rect.top += 5
        top_pipe_collision_rect.bottom -= 5

        bottom_pipe_collision_rect.left += 5
        bottom_pipe_collision_rect.right -= 5
        bottom_pipe_collision_rect.top += 5
        bottom_pipe_collision_rect.bottom -= 5

        # Check for collision with top pipe
        if bird_collision_rect.colliderect(top_pipe_collision_rect):
            return True

        # Check for collision with bottom pipe
        if bird_collision_rect.colliderect(bottom_pipe_collision_rect):
            return True

    if bird_y < 0 or bird_y > WINDOW_HEIGHT:
        return True

    return False


 








def update_score():
    global score
    for pipe in pipe_list:
        if pipe["x"] < bird_x and not pipe["scored"]:
            score += 1
            pipe["scored"] = True

def draw_score():
    score_surface = font.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH/2, 50))
    game_display.blit(score_surface, score_rect)

# Draw graphics
def draw():
    game_display.blit(background_img, (0, 0))
    draw_pipes()
    draw_bird()
    draw_score()
    pygame.display.update()

# Draw the home screen
def draw_home():
    game_display.blit(background_img, (0, 0))
    title_text = font.render("Flappy Bird", True, (0, 0, 0))  # Black font color
    start_text = font.render("Press SPACE to Start", True, (0, 0, 0))  # Black font color
    title_x = (WINDOW_WIDTH - title_text.get_width()) // 2
    title_y = WINDOW_HEIGHT // 4
    start_x = (WINDOW_WIDTH - start_text.get_width()) // 2
    start_y = WINDOW_HEIGHT // 2
    game_display.blit(title_text, (title_x, title_y))
    game_display.blit(start_text, (start_x, start_y))
    pygame.display.update()



# Main game loop
clock = pygame.time.Clock()
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if game_state == HOME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = PLAYING

        if game_state == PLAYING:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = -jump_strength

    if game_state == HOME:
        draw_home()
    elif game_state == PLAYING:
    
        # Update game state
        bird_velocity += gravity
        bird_y += bird_velocity
        move_pipes()
        add_pipe()
        update_score()
        game_over = check_collision()

        # Draw graphics
        game_display.blit(background_img, (0, 0))
        draw_pipes()
        draw_bird()
        draw_score()
        pygame.display.update()

        if game_over:
            # Optionally add a game-over screen
            game_state = HOME
            bird_y = 200
            bird_velocity = 0
            pipe_list.clear()
            score = 0
            pygame.time.delay(1000)  # Pause for 1 second after game over

    clock.tick(60)

pygame.qui
t()
sys.exit()
