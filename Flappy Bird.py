import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 400, 600
GROUND_HEIGHT = 100
BIRD_SIZE = 40
PIPE_WIDTH = 60
PIPE_GAP = 200
GRAVITY = 0.8
FLAP_STRENGTH = 10
PIPE_SPEED = 3  # Speed at which pipes move towards the bird
COUNTDOWN_TIME = 3 * 1000  # 3 seconds

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Initialize clock
clock = pygame.time.Clock()

# Load bird image
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))

# Game variables
bird_x = WIDTH // 4
bird_y = HEIGHT // 2
bird_velocity = 0
score = 0
game_over = False
paused = False
countdown_start_time = pygame.time.get_ticks() + COUNTDOWN_TIME
PIPE_HEIGHT = random.randint(100, 400)  # Initial pipe height

# Initial pipe position
pipe_x = WIDTH
PIPE_HEIGHT = random.randint(100, 400)

def reset_game():
    """Reset all game variables to initial state"""
    global bird_x, bird_y, bird_velocity, score, game_over, paused, countdown_start_time, pipe_x, PIPE_HEIGHT
    bird_x = WIDTH // 4
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    game_over = False
    paused = False
    countdown_start_time = pygame.time.get_ticks() + COUNTDOWN_TIME
    pipe_x = WIDTH
    PIPE_HEIGHT = random.randint(100, 400)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not paused:
                bird_velocity = -FLAP_STRENGTH
            elif event.key == pygame.K_p and not game_over:
                paused = not paused
            elif event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        current_time = pygame.time.get_ticks()

        # Countdown before starting the game
        if current_time < countdown_start_time:
            screen.fill(WHITE)
            countdown = 4 - ((countdown_start_time - current_time) // 1000)
            font = pygame.font.Font(None, 72)
            countdown_text = font.render(str(countdown), True, GREEN)
            screen.blit(countdown_text, ((WIDTH - countdown_text.get_width()) // 2, (HEIGHT - countdown_text.get_height()) // 2))

            # Display controls
            controls_font = pygame.font.Font(None, 24)
            controls_text = [
                "Controls:",
                "SPACE - Flap",
                "P - Pause/Resume",
                "R - Restart (when game over)"
            ]
            for i, text in enumerate(controls_text):
                control_surface = controls_font.render(text, True, GREEN)
                screen.blit(control_surface, (10, 10 + i * 25))
        else:
            if not paused:
                # Bird only moves vertically, not horizontally
                bird_velocity += GRAVITY
                bird_y += bird_velocity

                # Check for collisions
                if bird_y < 0 or bird_y > HEIGHT - GROUND_HEIGHT:
                    game_over = True

                # Move pipes towards the bird
                pipe_x -= PIPE_SPEED

                if pipe_x < -PIPE_WIDTH:
                    pipe_x = WIDTH
                    PIPE_HEIGHT = random.randint(100, 400)
                    score += 1

                # Check for collisions with pipes
                if bird_x < pipe_x + PIPE_WIDTH and bird_x + BIRD_SIZE > pipe_x:
                    if bird_y < PIPE_HEIGHT or bird_y + BIRD_SIZE > PIPE_HEIGHT + PIPE_GAP:
                        game_over = True

            # Draw everything
            screen.fill(WHITE)
            pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, PIPE_HEIGHT))
            pygame.draw.rect(screen, GREEN, (pipe_x, PIPE_HEIGHT + PIPE_GAP, PIPE_WIDTH, HEIGHT - GROUND_HEIGHT - PIPE_HEIGHT - PIPE_GAP))
            pygame.draw.rect(screen, GREEN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
            screen.blit(bird_image, (bird_x, bird_y))

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, GREEN)
            screen.blit(score_text, (10, 10))

            # Display pause message if paused
            if paused:
                font = pygame.font.Font(None, 48)
                pause_text = font.render("PAUSED", True, GREEN)
                screen.blit(pause_text, ((WIDTH - pause_text.get_width()) // 2, (HEIGHT - pause_text.get_height()) // 2))
                instruction_font = pygame.font.Font(None, 24)
                instruction_text = instruction_font.render("Press P to resume", True, GREEN)
                screen.blit(instruction_text, ((WIDTH - instruction_text.get_width()) // 2, (HEIGHT - instruction_text.get_height()) // 2 + 50))

        pygame.display.update()
        clock.tick(30)
    else:
        # Game over screen
        screen.fill(WHITE)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, GREEN)
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2 - 50))

        # Display final score
        score_font = pygame.font.Font(None, 36)
        final_score_text = score_font.render(f"Final Score: {score}", True, GREEN)
        screen.blit(final_score_text, ((WIDTH - final_score_text.get_width()) // 2, (HEIGHT - final_score_text.get_height()) // 2))

        # Display restart instruction
        instruction_font = pygame.font.Font(None, 24)
        restart_text = instruction_font.render("Press R to restart", True, GREEN)
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, (HEIGHT - restart_text.get_height()) // 2 + 50))

        pygame.display.update()
        clock.tick(30)

pygame.quit()
sys.exit()
