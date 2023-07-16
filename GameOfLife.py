import pygame
from threading import Thread
import time

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
BLOCK_SIZE = 5
FPS_CAP = 60

# Global game parameters
alive_blocks = []
started = False
clock = pygame.time.Clock()

def get_neighbours(x: int, y: int) -> list[list[int]]:
	neighbours = []

	for x_off in range(-1, 2):
		for y_off in range(-1, 2):
			if not (x_off == 0 and y_off == 0): # x_off = 0 and y_off = 0 means current block, so not a neighbour
				neighbours.append([x + x_off, y + y_off])

	return neighbours

def game_of_life():
	global alive_blocks
	
	next_blocks = []

	for b in alive_blocks: # Loop over only the alive blocks, as dead blocks with dead neighbours will remain unchanged
		neighbours = get_neighbours(b[0], b[1])

		for n in neighbours:
			n_neighbours = get_neighbours(n[0], n[1])
			n_neighbours.remove(b)

			alive = 1

			for n_n in n_neighbours:
				if n_n in alive_blocks:
					alive += 1

			if alive == 3 and not n in next_blocks:
				next_blocks.append(n)
			elif n in alive_blocks and alive == 2 and not n in next_blocks:
				next_blocks.append(n)

	alive_blocks = next_blocks

def run_simulation():
	while started:
		time.sleep(0.5)
		game_of_life()

def main():
	global board, started

	pygame.init()
	pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

	surface = pygame.display.get_surface()
	blank = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

	while True:
		pygame.draw.rect(surface, (0, 0, 0), blank) # Clear screen

		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Quit event
				pygame.quit()
				exit(0)

			elif event.type == pygame.KEYDOWN: # Key pressed events
				if event.key == pygame.K_ESCAPE: # Escape Key
					pygame.quit()
					exit(0)
				if event.key == pygame.K_s: # S Key
					started = not started

					if started:
						game_thread = Thread(target=run_simulation, daemon=True)
						game_thread.start()
				elif event.key == pygame.K_c: # C Key
					alive_blocks.clear()

			elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse button pressed events
				if event.button == 1 and not started: # Left click
					pos = [int(p / BLOCK_SIZE) for p in event.pos]

					if pos in alive_blocks:
						alive_blocks.remove(pos)
					else:
						alive_blocks.append(pos)

		for b in alive_blocks: # Draw all alive blocks
			rect = pygame.Rect(b[0] * BLOCK_SIZE, b[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
			pygame.draw.rect(surface, (255, 255, 255), rect)

		pygame.display.update()
		clock.tick(FPS_CAP)

if __name__ == '__main__':
	main()
