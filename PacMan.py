import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")

# Load font
font = pygame.font.Font(None, 36)

# Function to render score
def display_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# Pellets
pellets = [(100, 100), (200, 100), (300, 100), (400, 100),
           (100, 200), (200, 200), (300, 200), (400, 200),
           (100, 300), (200, 300), (300, 300), (400, 300)]

# Score
score = 0

# Class for Ghosts
class Ghost:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        self.direction = [0, 0]

# Create Ghosts
ghosts = [
    Ghost(100, 200, 4),
    Ghost(200, 200, 4),
    Ghost(300, 200, 4),
    Ghost(400, 200, 4)
]

# Define the maze using a 2D array
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Game loop
clock = pygame.time.Clock()
pacman_pos = [WIDTH // 2, HEIGHT // 2]
pacman_speed = 5
pacman_direction = [0, 0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_direction = [-pacman_speed, 0]
            elif event.key == pygame.K_RIGHT:
                pacman_direction = [pacman_speed, 0]
            elif event.key == pygame.K_UP:
                pacman_direction = [0, -pacman_speed]
            elif event.key == pygame.K_DOWN:
                pacman_direction = [0, pacman_speed]

    # Move Pac-Man
    pacman_pos[0] += pacman_direction[0]
    pacman_pos[1] += pacman_direction[1]

    # Boundary constraints for Pac-Man
    pacman_pos[0] = max(0, min(pacman_pos[0], WIDTH - 30))
    pacman_pos[1] = max(0, min(pacman_pos[1], HEIGHT - 30))

    # Check for collisions with walls (maze) for Pac-Man
    pacman_rect = pygame.Rect(pacman_pos[0], pacman_pos[1], 30, 30)
    for pellet_pos in pellets[:]:
        if pacman_rect.colliderect(pygame.Rect(pellet_pos[0], pellet_pos[1], 10, 10)):
            pellets.remove(pellet_pos)
            score += 10

    # Clear the screen
    screen.fill(BLACK)

    # Draw Pellets
    for pellet_pos in pellets:
        pygame.draw.circle(screen, WHITE, pellet_pos, 5)

    # Draw Pac-Man
    pacman = pygame.draw.circle(screen, YELLOW, (pacman_pos[0] + 15, pacman_pos[1] + 15), 15)

    # Move and draw ghosts
    for ghost in ghosts:
        ghost.rect.x += ghost.direction[0]
        ghost.rect.y += ghost.direction[1]

        # Boundary constraints for ghosts
        if ghost.rect.x < 0 or ghost.rect.x > WIDTH - 30:
            ghost.direction[0] *= -1
        if ghost.rect.y < 0 or ghost.rect.y > HEIGHT - 30:
            ghost.direction[1] *= -1

        # Check for collisions between Pac-Man and ghosts
        if pacman_rect.colliderect(ghost.rect):
            running = False  # Game Over

        # Draw ghosts
        pygame.draw.circle(screen, RED, (ghost.rect.x + 15, ghost.rect.y + 15), 15)

    # Display score
    display_score()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # After drawing pellets inside the game loop
    if not pellets:
        # Respawn Pac-Man
        pacman_pos = [WIDTH // 2, HEIGHT // 2]

        # Respawn Pellets
        pellets = [(100, 100), (200, 100), (300, 100), (400, 100),
                   (100, 200), (200, 200), (300, 200), (400, 200),
                   (100, 300), (200, 300), (300, 300), (400, 300)]

        # Reset Score
        score = 0

# Quit the game
pygame.quit()
sys.exit()

