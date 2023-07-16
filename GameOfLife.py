import pygame
from copy import deepcopy

'''
-------------=[ Conway's Game of Life ]=------------- 

Rules (from https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life):
	Any live cell with fewer than two live neighbours dies, as if by underpopulation.
	Any live cell with two or three live neighbours lives on to the next generation.
	Any live cell with more than three live neighbours dies, as if by overpopulation.
	Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

-----------------------------------------------------
'''

board_x = 750
board_y = 750
pixel_size = 10
started = False

board_pixels_x = int(board_x / pixel_size)
board_pixels_y = int(board_y / pixel_size)

board = [
	[0 for x in range(board_pixels_x)] for y in range(board_pixels_y)
]

def is_in_bounds(x: int, y: int):
	return x >= 0 and x < board_pixels_x and y >= 0 and y < board_pixels_y

def get_neighbours(x: int, y: int) -> list[tuple[int]]:
	neighbours = []

	for x_off in range(-1, 2):
		for y_off in range(-1, 2):
			if x_off == 0 and y_off == 0:
				pass
			elif is_in_bounds(x + x_off, y + y_off):
				neighbours.append((x + x_off, y + y_off))

	return neighbours

def game_of_life():
	global board

	cpy = deepcopy(board)
	
	for x in range(board_pixels_x):
		for y in range(board_pixels_y):
			alive = 0

			for n in get_neighbours(x, y):
				if board[n[1]][n[0]]:
					alive += 1

			if board[y][x]:
				if alive < 2 or alive > 3:
					cpy[y][x] = 0
			elif alive == 3:
				cpy[y][x] = 1

	board = cpy

def main():
	global board, started

	pygame.init()
	pygame.display.set_mode((board_x, board_y))

	surface = pygame.display.get_surface()
	blank = pygame.Rect(0, 0, board_x, board_y)
	copy_board = []

	while True:
		pygame.draw.rect(surface, (0, 0, 0), blank)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					if started:
						board = copy_board
					else:
						copy_board = deepcopy(board)

					started = not started
				elif event.key == pygame.K_c:
					board = [
						[0 for x in range(board_pixels_x)] for y in range(board_pixels_y)
					]

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if not started:
					pos = event.pos
					board[int(pos[1] / pixel_size)][int(pos[0] / pixel_size)] = int(not board[int(pos[1] / pixel_size)][int(pos[0] / pixel_size)])

		if started:
			game_of_life()

		for y in range(board_pixels_y):
			for x in range(board_pixels_x):
				if board[y][x]:
					rect = pygame.Rect(x * pixel_size, y * pixel_size, pixel_size, pixel_size)
					pygame.draw.rect(surface, (255, 255, 255), rect)

		pygame.display.update()

if __name__ == '__main__':
	main()
