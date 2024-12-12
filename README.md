The solution to the problem involves developing a grid-based simulation using Pygame, where 
both a user-controlled agent and an AI-controlled agent navigate through a maze-like grid 
environment filled with obstacles and dynamic threats. The primary goal is for the agents to 
reach a predefined finish line while minimizing penalties, such as point deductions for 
unnecessary moves or collisions with zombies.
The grid is designed as a fixed-size space divided into cells. Each cell can represent an empty 
space, a wall, or be occupied by a zombie or an agent. The walls are randomly generated and 
connected, forming complex paths that require strategic movement. This setup mimics realworld scenarios where navigation is constrained by barriers, adding complexity to the task.
The red agent is the user controlled and the purple agent is AI agent. The total energy in the 
start of each program is 5000 and with each move 10 points are deducted. On collision with a 
zombie 100 points are deducted. The AI-controlled agent, employs the A* search algorithm to 
calculate the optimal path to the finish line. The algorithm uses a heuristic based on Manhattan 
distance to estimate the cost of reaching the goal and adjusts its calculations to avoid zombieadjacent cells by assigning higher costs to such positions.
