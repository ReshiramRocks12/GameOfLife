import pygame
from threading import Thread
import math

'''
-------------=[ Conway's Game of Life ]=------------- 

Rules (from https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life):
	Any live cell with fewer than two live neighbours dies, as if by underpopulation.
	Any live cell with two or three live neighbours lives on to the next generation.
	Any live cell with more than three live neighbours dies, as if by overpopulation.
	Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

-----------------------------------------------------
'''

# Changable parameters
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750
BLOCK_SIZE = 10
FPS_LIMIT = 60
MAX_CAMERA_SPEED = 60
SIMULATIONS_PER_SECOND = 10

# Global game parameters
alive_blocks = []
started = False
camera = [0, 0]
view_offset = [0, 0]

def get_neighbours(x: int, y: int) -> list[list[int]]:
	neighbours = []

	for x_off in range(-1, 2):
		for y_off in range(-1, 2):
			if not (x_off == 0 and y_off == 0): # x_off = 0 and y_off = 0 means current block, so not a neighbour
				neighbours.append([x + x_off, y + y_off])

	return neighbours

def game_of_life() -> None:
	global alive_blocks, started
	
	next_blocks = []

	for b in alive_blocks: # Loop over only the alive blocks, as dead blocks with dead neighbours will remain unchanged
		neighbours = get_neighbours(b[0], b[1])

		for n in neighbours: # Loop over the neighbours of the alive block
			n_neighbours = get_neighbours(n[0], n[1])
			n_neighbours.remove(b) # Remove b as it is already known to be alive

			alive = 1 # Set to 1 as it has at least 1 alive neighbour already

			for n_n in n_neighbours: # Look at the neighbour's neighbours and count the alive blocks around it
				if n_n in alive_blocks:
					alive += 1

			if alive == 3 and not n in next_blocks:
				next_blocks.append(n)
			elif n in alive_blocks and alive == 2 and not n in next_blocks:
				next_blocks.append(n)
	
	if started:
		alive_blocks = next_blocks

def run_simulation() -> None:
	global started	

	sim_clock = pygame.time.Clock()

	while started:
		game_of_life()
		sim_clock.tick(SIMULATIONS_PER_SECOND)
		
def on_key_down(key: int) -> None:
	global camera, MAX_CAMERA_SPEED, started, view_offset

	if key == pygame.K_ESCAPE: # Escape Key
		pygame.quit()
		exit(0)
		
	elif key == pygame.K_SPACE: # Space Key
		started = not started

		if started:
			game_thread = Thread(target=run_simulation, daemon=True)
			game_thread.start()
			
	elif key == pygame.K_c: # C Key
		started = False
		alive_blocks.clear()
		view_offset = [0, 0]
	
	if alive_blocks:
		if key == pygame.K_w: # W Key
			camera[1] = max(camera[1] - MAX_CAMERA_SPEED, -MAX_CAMERA_SPEED)
		elif key == pygame.K_s: # S Key
			camera[1] = min(camera[1] + MAX_CAMERA_SPEED, MAX_CAMERA_SPEED)
		elif key == pygame.K_a: # A Key
			camera[0] = max(camera[0] - MAX_CAMERA_SPEED, -MAX_CAMERA_SPEED)
		elif key == pygame.K_d: # D Key
			camera[0] = min(camera[0] + MAX_CAMERA_SPEED, MAX_CAMERA_SPEED)
			
def on_key_up(key: int) -> None:
	global camera, MAX_CAMERA_SPEED
	
	if key == pygame.K_w: # W Key
		camera[1] = max(0, camera[1] + MAX_CAMERA_SPEED)
	elif key == pygame.K_s: # S Key
		camera[1] = min(0, camera[1] - MAX_CAMERA_SPEED)
	elif key == pygame.K_a: # A Key
		camera[0] = max(0, camera[0] + MAX_CAMERA_SPEED)
	elif key == pygame.K_d: # D Key
		camera[0] = min(0, camera[0] - MAX_CAMERA_SPEED)
		
def draw_blocks(surface: pygame.Surface) -> None:
	for block in alive_blocks: # Draw all alive blocks
		rect = pygame.Rect((block[0] - view_offset[0]) * BLOCK_SIZE, (block[1] - view_offset[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
		pygame.draw.rect(surface, (255, 255, 255), rect)
	
def main() -> None:
	global camera, started, view_offset

	pygame.init()
	pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	
	clock = pygame.time.Clock()

	surface = pygame.display.get_surface()
	blank = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

	while True:
		pygame.draw.rect(surface, (0, 0, 0), blank) # Clear screen

		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Quit event
				pygame.quit()
				exit(0)

			elif event.type == pygame.KEYDOWN: # Key pressed events
				on_key_down(event.key)
					
			elif event.type == pygame.KEYUP: # Key depressed events
				on_key_up(event.key)

		fps = clock.get_fps()
		view_offset[0] += camera[0] / (fps if fps > 0 else MAX_CAMERA_SPEED)
		view_offset[1] += camera[1] / (fps if fps > 0 else MAX_CAMERA_SPEED)
		
		mouse_buttons = pygame.mouse.get_pressed()
		
		if not started and (mouse_buttons[0] or mouse_buttons[2]):
			pos = list(pygame.mouse.get_pos())
			pos[0] = math.floor(pos[0] / BLOCK_SIZE + view_offset[0])
			pos[1] = math.floor(pos[1] / BLOCK_SIZE + view_offset[1])

			if pos in alive_blocks:
				if mouse_buttons[2]:
					alive_blocks.remove(pos)
			elif mouse_buttons[0]:
				alive_blocks.append(pos)

		draw_blocks(surface)
		
		pygame.display.update()
		clock.tick(FPS_LIMIT)

if __name__ == '__main__':
	main()
