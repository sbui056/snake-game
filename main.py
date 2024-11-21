import pygame
import time
import random

# Defining variables
snake_speed = 15  # Speed of the snake
fps = pygame.time.Clock()  # Control frame rate
black = pygame.Color(0, 0, 0)  # Color for snake body
white = pygame.Color(255, 255, 255)  # Color for the fruit
red = pygame.Color(255, 0, 0)  # Color for game over text
green = pygame.Color(0, 255, 0)  # Background color

# Initialize Pygame
pygame.init()

# Initialize pygame mixer for sound effects
pygame.mixer.init()
apple_crunch_sound = pygame.mixer.Sound("assets/sounds/apple_crunch_sound.wav")  # Sound when fruit is eaten

# Set up the display window
window_x = 720  # Window width
window_y = 480  # Window height
screen = pygame.display.set_mode((window_x, window_y))  # Create window
pygame.display.set_caption("Pygame Snake Game!")  # Set window title

# Initialize the snake's position and body
snake_position = [100, 50]  # Snake starts at position (100, 50)
snake_body = [
                [100, 50],  # Initial body of the snake
                [90, 50],
                [80, 50],
                [70, 50]
            ]
direction = 'RIGHT'  # Snake initially moves to the right
change_to = direction  # Variable to track direction change

# Initialize fruit position and spawn state
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True  # Whether or not the fruit spawns

# Set up initial score
score = 0

# Function to display the score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)  # Set font and size for the score
    score_surface = score_font.render('Score: ' + str(score), True, color)  # Render score text
    score_rect = score_surface.get_rect()  # Get the rectangle for placing the score on screen
    screen.blit(score_surface, score_rect)  # Blit (draw) the score on the screen

# Function to handle game over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)  # Font for game over text
    game_over_surface = my_font.render('Your score is: ' + str(score), True, red)  # Render game over text
    game_over_rect = game_over_surface.get_rect()  # Get the position of the game over text
    game_over_rect.midtop = (screen.get_width() // 2, screen.get_height() // 4)  # Center the text
    screen.blit(game_over_surface, game_over_rect)  # Blit the game over text to the screen
    pygame.display.flip()  # Update the display
    time.sleep(3)  # Wait for 2 seconds before quitting
    pygame.quit()  # Close Pygame
    quit()  # Exit the game

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        # Capture key presses for direction changes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
    
    # Prevent the snake from going in the opposite direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Update the snake's position based on the direction
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Add the new head position to the snake's body
    snake_body.insert(0, list(snake_position))

    # Check if snake has eaten the fruit
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10  # Increase score
        apple_crunch_sound.play()  # Play fruit crunch sound
        fruit_spawn = False  # Fruit needs to respawn
    else:
        snake_body.pop()  # Remove the last segment of the snake (snake doesn't grow if it hasn't eaten fruit)

    # Respawn the fruit if it's been eaten
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True  # Set fruit_spawn to True to spawn a new fruit

    screen.fill(black)  # Fill the screen with green (background)

    # Draw the snake
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the fruit
    pygame.draw.rect(screen, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Check if snake hits the wall
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()  # Game over if the snake hits the wall horizontally
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()  # Game over if the snake hits the wall vertically

    # Check if the snake hits its own body
    for block in snake_body[1:]:  # Skip the first block (head)
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()  # Game over if the snake hits itself

    # Display the score
    show_score(1, white, 'times new roman', 20)

    # Update the display
    pygame.display.update()

    # Control the frame rate (speed of the game)
    fps.tick(snake_speed)

# Quit Pygame when the game loop ends
pygame.quit()