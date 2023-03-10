import pygame
import sys
import random
from pygame import font

# Set up pygame window
pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption('Vertical Scrolling Game')

# Set up game clock
clock = pygame.time.Clock()

# Set up player sprite
player_image = pygame.Surface((20, 30))
player_image.fill((0, 0, 255))
player_rect = player_image.get_rect()
player_rect.center = (300, 400)

# Set up obstacle sprite
#width1 = random.randint(20, 200)
obstacle_image = pygame.Surface((60, 20))
obstacle_image.fill((255, 0, 0))

# Set up obstacles list
obstacles = []

# Set up obstacle generation timer
obstacle_timer = 1

# Set up gravity and upward thrust
gravity = 1
upward_thrust = -30
obstacle_gravity = 5 * gravity

# Set up game over screen font
font = pygame.font.Font(None, 36)



# Set up player movement variables
x_velocity = 0  # Initialize x velocity to 0
y_velocity = 0  # Initialize y velocity to 0
acceleration = 10
max_velocity = 20
friction = 0.9  # Add friction to slow down player when not accelerating

# Set up game over flag
game_over = False


# Set up game loop
while True:
    score = 0   # Set score to 0 at the start of the game
    # Update score for every obstacle passed
    for obstacle in obstacles:
        if obstacle.top > player_rect.bottom:
            score += 5
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y_velocity -= acceleration
            elif event.key == pygame.K_a:
                x_velocity -= acceleration
            elif event.key == pygame.K_s:
                y_velocity += acceleration
            elif event.key == pygame.K_d:
                x_velocity += acceleration
            elif event.key == pygame.K_r:  # Restart game on 'r' key press
                player_rect.center = (300, 400)
                obstacles = []
                obstacle_timer = 0
                game_over = False
                score = 0
        elif event.type == pygame.KEYUP:  # Stop player acceleration on key release
            if event.key in (pygame.K_w, pygame.K_s):
                y_velocity = 0
            elif event.key in (pygame.K_a, pygame.K_d):
                x_velocity = 0
    
    # Get list of keys being pressed
    keys = pygame.key.get_pressed()

    # Generate obstacles
    obstacle_timer += 1
    if obstacle_timer % 60 == 0:
        x = random.randint(0, 550)  # Generate random x position between 0 and 280
        #width = random.randint(20, 150)
        obstacle = pygame.Rect(x, 0, 60, 20)  # Create obstacle rect
        obstacles.append(obstacle)  # Add obstacle to list

    # Apply friction to player
    x_velocity *= friction
    y_velocity *= friction
   
    # Limit player velocity
    if x_velocity > max_velocity:
        x_velocity = max_velocity
    elif x_velocity < -max_velocity:
        x_velocity = -max_velocity
    if y_velocity > max_velocity:
        y_velocity = max_velocity
    elif y_velocity < -max_velocity:
        y_velocity = -max_velocity

   # Apply gravity to player and obstacles
    player_rect.y += gravity
    for obstacle in obstacles:
        obstacle.y += obstacle_gravity

    # Check for collisions
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            game_over = True  # Set game over flag

    # End game if player goes out of bounds
    if player_rect.top < 0 or player_rect.bottom > 800 or player_rect.left > 600 or player_rect.right > 600:
        game_over = True  # Set game over flag

    # Check for game over
    if game_over:
        # Display game over screen
        game_over_text = font.render("Game Over!", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (300, 400)
        screen.blit(game_over_text, game_over_rect)
        play_again_text = font.render("Press 'R' to Play Again", True, (255, 255, 255))
        play_again_rect = play_again_text.get_rect()
        play_again_rect.center = (300, 450)
        screen.blit(play_again_text, play_again_rect)

        pygame.display.flip()  # Update display

        # Wait for 'r' key press to restart game
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        player_rect.center = (300, 400)  # Reset player position
                        obstacles = []  # Clear obstacles
                        obstacle_timer = 0  # Reset obstacle timer
                        game_over = False  # Reset game over flag
    else:
        # Clear screen
        screen.fill((0, 0, 0))

         # Move player based on velocity
        player_rect.x += int(x_velocity)
        player_rect.y += int(y_velocity)


        # Draw player
        screen.blit(player_image, player_rect)

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle_image, obstacle)

             # Display score on screen
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_text, score_rect)

        # Update display
    pygame.display.flip()
           

    # Limit frame rate
    clock.tick(60)

