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
blue = pygame.Color(50, 50, 255)
gray = pygame.Color(169, 169, 169) 

import heapq
ai_mode = False

# messing with ai
# Function to draw the ai toggle button
def draw_button():
    button_color = blue if ai_mode else gray
    font = pygame.font.SysFont('times new roman', 30)
    button_surface = font.render('AI Mode', True, white)
    button_rect = pygame.Rect(window_x - 145, 20, 120, 40)
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_surface, (window_x - 140, 25))
    return button_rect

# messing around with A*
def astar(start, goal, snake_body):
    grid_size = (window_x // 10, window_y // 10)  # Grid dimensions
    directions = [(0, -10), (0, 10), (-10, 0), (10, 0)]  # Possible moves: up, down, left, right

    # Heuristic: Manhattan distance
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Priority queue and other data structures
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, node)
    came_from = {}
    g_score = {start: 0}  # Cost to reach each node
    f_score = {start: heuristic(start, goal)}  # Estimated total cost

    while open_set:
        _, current = heapq.heappop(open_set)

        # Check if we've reached the goal
        if current == goal:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)

            # Check bounds and avoid the snake's body
            if (0 <= neighbor[0] < window_x and 0 <= neighbor[1] < window_y and
                neighbor not in snake_body):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return an empty path if no solution exists

# reset game function
def reset_game():
    global snake_position, snake_body, direction, change_to, score, fruit_position, fruit_spawn, game_over_flag, snake_speed
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    game_over_flag = False  # Reset the game over flag
    snake_speed = 15

# Initialize Pygame
pygame.init()

# Initialize pygame mixer for sound effects
pygame.mixer.init()

apple_crunch_sound = pygame.mixer.Sound("assets/sounds/apple_crunch_sound.wav")  # Sound when fruit is eaten
bump_sound = pygame.mixer.Sound("assets/sounds/bump_sound.wav")
snake_move_sound = pygame.mixer.Sound("assets/sounds/snake_move_sound.mp3")

pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1) #play indefinitely

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
    global game_over_flag  # Make sure to modify the global flag
    if not game_over_flag:  # If the game is not already over
        bump_sound.play()  # Play the bump sound
        game_over_flag = True  # Set the game over flag to True

    my_font = pygame.font.SysFont('times new roman', 50)  # Font for game over text
    game_over_surface = my_font.render('Your score is: ' + str(score), True, red)  # Render game over text
    game_over_rect = game_over_surface.get_rect()  # Get the position of the game over text
    game_over_rect.midtop = (screen.get_width() // 2, screen.get_height() // 4)  # Center the text
    screen.blit(game_over_surface, game_over_rect)  # Blit the game over text to the screen

    # Render and display the "Press 'R' to restart" message
    restart_surface = my_font.render('Press "R" to restart', True, red)
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (screen.get_width() // 2, screen.get_height() // 2)  # Position below the game over message
    screen.blit(restart_surface, restart_rect)  # Blit the restart message

    pygame.display.flip()  # Update the display

# Main game loop
game_over_flag = False  # This flag will be used to check if the game is over
running = True
previous_direction = None
while running:
    screen.fill(black)  # Fill the screen with black (background)
    button_rect = draw_button()  # Draw AI mode button


    if game_over_flag:  # If the game is over, display the game over screen and wait for a restart
        game_over()  # Display game over
        pygame.display.update()  # Update the screen

        # Check for restart key press ('R')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to restart the game
                    reset_game()  # Reset all game variables
                    running = True  # Restart the game loop
                    break  # Exit the event loop to restart

        continue  # Skip the rest of the loop while waiting for restart

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                ai_mode = not ai_mode
        
        # Handle restart game with the 'R' key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'R' to restart the game
                reset_game()

        if event.type == pygame.KEYDOWN and not ai_mode:
            if event.key == pygame.K_UP and direction != 'DOWN' and direction != 'UP':  # Only play sound if direction changes
                change_to = 'UP'
                snake_move_sound.play()
            if event.key == pygame.K_DOWN and direction != 'UP' and direction != 'DOWN':  # Only play sound if direction changes
                change_to = 'DOWN'
                snake_move_sound.play()
            if event.key == pygame.K_LEFT and direction != 'RIGHT' and direction != 'LEFT':  # Only play sound if direction changes
                change_to = 'LEFT'
                snake_move_sound.play()
            if event.key == pygame.K_RIGHT and direction != 'LEFT' and direction != 'RIGHT':  # Only play sound if direction changes
                change_to = 'RIGHT'
                snake_move_sound.play()
    
    # Prevent the snake from going in the opposite direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # ai mess
    # Move the snake (AI or manual)
    if ai_mode:
        path = astar(tuple(snake_position), tuple(fruit_position), set(map(tuple, snake_body)))
        if path:
            next_position = path[0]
            if next_position[0] > snake_position[0]:
                direction = 'RIGHT'
            elif next_position[0] < snake_position[0]:
                direction = 'LEFT'
            elif next_position[1] > snake_position[1]:
                direction = 'DOWN'
            elif next_position[1] < snake_position[1]:
                direction = 'UP'
        # Play sound only if the direction changes
            if  direction != previous_direction:
                direction = direction  # Update direction to new direction
                snake_move_sound.play()  # Play sound when AI moves
                previous_direction = direction  # Update previous direction

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
        score += 1  # Increase score
        # Example: Increasing speed as score increases
        if score >= 1:
            snake_speed += 1  # Speed up each fruit eaten
        apple_crunch_sound.play()  # Play fruit crunch sound
        fruit_spawn = False  # Fruit needs to respawn
    else:
        snake_body.pop()  # Remove the last segment of the snake (snake doesn't grow if it hasn't eaten fruit)

    # Respawn the fruit if it's been eaten
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True  # Set fruit_spawn to True to spawn a new fruit

    # Draw the snake
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the fruit
    pygame.draw.rect(screen, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Check if snake hits the wall
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        bump_sound.play()
        game_over()  # Game over if the snake hits the wall horizontally
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        bump_sound.play()
        game_over()  # Game over if the snake hits the wall vertically

    # Check if the snake hits its own body
    for block in snake_body[1:]:  # Skip the first block (head)
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            bump_sound.play()
            game_over()  # Game over if the snake hits itself

    # Display the score
    show_score(1, white, 'DejaVu Sans', 40)

    # Update the display
    pygame.display.update()

    # Control the frame rate (speed of the game)
    fps.tick(snake_speed)

# Quit Pygame when the game loop ends
pygame.quit()