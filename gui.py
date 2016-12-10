#! /usr/bin/env python
# gui.py

"""This script provides two functions for drawing the board and
printing any message over the screen
"""

import pygame

SIZE = 450
SCREEN = pygame.display.set_mode((SIZE, SIZE), 0, 32)

def draw_board(board, size, grid_length):
    """Draws the Tic Tac Toe board"""
    black = (0, 0, 0)
    white = (255, 255, 255)

    SCREEN.fill(white)

    for i in range(grid_length):
        for j in range(grid_length):
            start_point = (j * SIZE / grid_length, i * SIZE / grid_length)
            size_rect = (SIZE / grid_length, SIZE / grid_length)
            pygame.draw.rect(
                SCREEN, black, (start_point, size_rect), 4)

    for i in range(grid_length):
        for j in range(grid_length):
            if board[i][j] == 1:
                # drawing a circle
                x_coord = (SIZE / (2 * grid_length)) * ((2 * j) + 1)
                y_coord = (SIZE / (2 * grid_length)) * ((2 * i) + 1)
                radius = SIZE / (2 * grid_length) - 4
                pygame.draw.circle(SCREEN, black, (xcoord, y_coord), radius, 4)

            elif board[i][j] == 0:
                # drawing a cross
                first_point = (j * SIZE / grid_length + 5, i * SIZE / grid_length + 5)
                second_point = ((j + 1) * SIZE / grid_length - 5, (i + 1) * SIZE / grid_length - 5)
                pygame.draw.line(SCREEN, black, first_point, second_point, 4)

                first_point = ((j + 1) * SIZE / grid_length - 5, i * SIZE / grid_length + 5)
                second_point = (j * SIZE / grid_length + 5, (i + 1) * SIZE / grid_length - 5)
                pygame.draw.line(SCREEN, black, first_point, second_point, 4)

    pygame.display.update()


def display_message(msg):
    """Displays any message provided in argument"""
    blue = (0, 0, 200)

    font = pygame.font.SysFont(None, 50)

    label = font.render(msg, True, blue)

    x_width = (screen.get_rect().width - label.get_rect().width) / 2
    y_width = (screen.get_rect().height - label.get_rect().height) / 2

    SCREEN.blit(label, (x_width, y_width))

    pygame.display.flip()

    pygame.time.wait(1000)
