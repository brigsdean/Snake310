import pygame
import random
import sys

# =============================================
# CSE 310 - Snake Game
# =============================================

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 180, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CSE 310 - Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 35)
score_font = pygame.font.SysFont("Arial", 25)

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT // 2
        self.body = [(self.x, self.y)]
        self.direction = (1, 0)  # Start moving right
        self.score = 0
        self.level = 1

    def move(self):
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        self.body.pop()  # Remove tail

    def grow(self):
        self.body.append(self.body[-1])  # Add one segment
        self.score += 10
        # Level up every 5 foods
        if self.score % 50 == 0:
            self.level += 1

    def change_direction(self, new_direction):
        # Prevent reversing direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Draw head slightly different
        pygame.draw.rect(screen, DARK_GREEN, 
                        (self.body[0][0] * GRID_SIZE, self.body[0][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    snake = Snake()
    food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.change_direction((1, 0))

        if not game_over:
            snake.move()

            # Check if ate food
            if snake.body[0] == food:
                snake.grow()
                food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

            if snake.check_collision():
                game_over = True

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        
        snake.draw()
        
        # Draw food
        pygame.draw.rect(screen, RED, 
                        (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Score and Level
        score_text = score_font.render(f"Score: {snake.score}   Level: {snake.level}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = score_font.render("Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()

        # Increase speed with level (additional requirement)
        speed = 8 + snake.level * 2
        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()