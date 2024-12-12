import pygame
import random
import heapq

# Initialize Pygame
pygame.init()

# Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
GRID_SIZE = 50
CELL_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) // GRID_SIZE
FPS = 5  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Runner")
screen.fill(WHITE)

# Draw the grid
def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_WIDTH, y))

# Zombie class
class Zombie:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, DARK_GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self, walls):
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Down, Up, Right, Left
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]

        # Ensure the zombie stays within bounds and  walls
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in walls:
            self.x = new_x
            self.y = new_y

# Agent class
class Agent:
    def __init__(self, x, y, color=RED):
        self.x = x
        self.y = y
        self.points = 5000
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self, direction, walls):
        dx, dy = 0, 0
        if direction == "UP":
            dx, dy = 0, -1
        elif direction == "DOWN":
            dx, dy = 0, 1
        elif direction == "LEFT":
            dx, dy = -1, 0
        elif direction == "RIGHT":
            dx, dy = 1, 0

        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in walls:
            self.x = new_x
            self.y = new_y
            self.points -= 10  

    def check_collision_with_zombies(self, zombies):
        for zombie in zombies:
            if self.x == zombie.x and self.y == zombie.y:
                self.points -= 100  

    def a_star(self, start, goal, walls, zombies):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

        open_list = []
        closed_list = set()
        came_from = {}

        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        heapq.heappush(open_list, (f_score[start], start))

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            closed_list.add(current)

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)

                if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in walls:
                    # Increase the cost for moving into zombie-dangerous cells
                    danger_penalty = 0
                    for zombie in zombies:
                        if abs(neighbor[0] - zombie.x) <= 1 and abs(neighbor[1] - zombie.y) <= 1:
                            danger_penalty = 100  

                    tentative_g_score = g_score.get(current, float('inf')) + 1 + danger_penalty
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return []

# Generate connected walls
def generate_walls(num_segments):
    walls = set()
    for _ in range(num_segments):
        start_x = random.randint(0, GRID_SIZE - 1)
        start_y = random.randint(0, GRID_SIZE - 1)
        segment_length = random.randint(4, 10)  
        direction = random.choice([(0, 1), (1, 0)])  # Horizontal or vertical

        for i in range(segment_length):
            x = start_x + (i * direction[0])
            y = start_y + (i * direction[1])
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                walls.add((x, y))
    return walls

# Draw walls
def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, BLACK, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Display points in the top-right corner
def draw_points(user_points, ai_points):
    font = pygame.font.Font(None, 36)
    user_points_text = font.render(f"User: {user_points}", True, BLUE)  # Changed color to BLUE
    ai_points_text = font.render(f"AI: {ai_points}", True, BLUE)  # Changed color to BLUE
    screen.blit(user_points_text, (WINDOW_WIDTH - 150, 10))
    screen.blit(ai_points_text, (WINDOW_WIDTH - 150, 40))

# Create zombies
zombies = [Zombie(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(50)]  #50 zombies

# Create connected walls
num_segments = 60  
walls = generate_walls(num_segments)

# Create agent
user_agent = Agent(0, 0, RED)  # User-controlled agent in red
ai_agent = Agent(0, 1, PURPLE)  # AI-controlled agent in purple

# Define finish line
finish_x, finish_y = GRID_SIZE - 1, GRID_SIZE - 1

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                user_agent.move("UP", walls)
            elif event.key == pygame.K_DOWN:
                user_agent.move("DOWN", walls)
            elif event.key == pygame.K_LEFT:
                user_agent.move("LEFT", walls)
            elif event.key == pygame.K_RIGHT:
                user_agent.move("RIGHT", walls)

    # Update zombie positions
    for zombie in zombies:
        zombie.move(walls)

    # Check for collision with zombies
    user_agent.check_collision_with_zombies(zombies)
    ai_agent.check_collision_with_zombies(zombies)

    # AI agent movement (A* pathfinding)
    ai_path = ai_agent.a_star((ai_agent.x, ai_agent.y), (finish_x, finish_y), walls, zombies)
    if ai_path:
        next_move = ai_path[0]  # Get next step in the path
        ai_agent.x, ai_agent.y = next_move
        ai_agent.points -= 10  

    # Check if both agents reached the finish line
    if user_agent.x == finish_x and user_agent.y == finish_y and ai_agent.x == finish_x and ai_agent.y == finish_y:
        print(f"User Agent reached the finish line with {user_agent.points} ENERGY.")
        print(f"AI Agent reached the finish line with {ai_agent.points} ENERGY.")
        running = False

    # Redraw screen
    screen.fill(WHITE)
    draw_grid()
    draw_walls(walls)
    for zombie in zombies:
        zombie.draw()
    user_agent.draw()
    ai_agent.draw()

    # Draw finish line
    pygame.draw.rect(screen, BLUE, (finish_x * CELL_SIZE, finish_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw points
    draw_points(user_agent.points, ai_agent.points)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()