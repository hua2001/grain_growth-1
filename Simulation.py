__author__ = 'steman'
import pygame
from cell import Cell
from grid import Grid

background_colour = (255, 255, 255)
(width, height) = (400, 400)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Grain growth')
screen.fill(background_colour)

pygame.display.flip()

running = True
grid = Grid(400, 400)
grid.random_embryo_loc(10)
while (not grid.full()):
	grid.pentagonal_random()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			screen.fill(background_colour)
			grid = Grid(400, 400)
			grid.random_embryo_loc(10)
			while (not grid.full()):
				grid.moore()
	screen.fill(background_colour)
	pix_arr = pygame.PixelArray(screen)
	for i in range(grid.rows):
		for j in range(grid.cols):
			if grid.board[i][j].id == 0:
				pix_arr[i][j] = pygame.Color(255, 0, 0)
			elif grid.board[i][j].id == 1:
				pix_arr[i][j] = pygame.Color(0, 255, 0)
			elif grid.board[i][j].id == 2:
				pix_arr[i][j] = pygame.Color(0, 0, 255)
			elif grid.board[i][j].id == 3:
				pix_arr[i][j] = pygame.Color(255, 255, 0)
			elif grid.board[i][j].id == 4:
				pix_arr[i][j] = pygame.Color(0, 255, 255)
			elif grid.board[i][j].id == 5:
				pix_arr[i][j] = pygame.Color(120, 0, 255)
			elif grid.board[i][j].id == 6:
				pix_arr[i][j] = pygame.Color(0, 120, 255)
			elif grid.board[i][j].id == 7:
				pix_arr[i][j] = pygame.Color(0, 0, 125)
			elif grid.board[i][j].id == 8:
				pix_arr[i][j] = pygame.Color(125, 0, 125)
			elif grid.board[i][j].id == 9:
				pix_arr[i][j] = pygame.Color(0, 0, 0)

	del pix_arr
	pygame.display.update()