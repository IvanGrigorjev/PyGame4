from pprint import pprint

import pygame
from random import randint

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 310, 460
FPS = 30


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Minesweeper(Board):
    def __init__(self, width, height, number_of_mines):
        super().__init__(width, height)
        self.number_of_mines = number_of_mines
        self.board = [[-1] * self.width for _ in range(self.height)]
        for _ in range(self.number_of_mines):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            self.board[y][x] = 10
        # pprint(self.board)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 10:
                    pygame.draw.rect(screen, 'red', (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                                     self.cell_size, self.cell_size))
                if 0 <= self.board[y][x] <= 8:
                    font = pygame.font.Font(None, (self.cell_size * 2) // 3)
                    text = font.render(str(self.board[y][x]), True, (0, 255, 0))
                    tab = self.cell_size // 15
                    screen.blit(text, (self.left + self.cell_size * x + tab, self.top + self.cell_size * y + tab))

                pygame.draw.rect(screen, 'white', (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                                   self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[1] < self.left + self.height * self.cell_size and \
                self.top <= mouse_pos[0] < self.top + self.width * self.cell_size:
            return (int((mouse_pos[1] - self.left) / self.cell_size), int((mouse_pos[0] - self.top) / self.cell_size))
        else:
            return None

    # метод изменяет поле, опираясь на полученные координаты клетки
    def on_click(self, cell_coords):
        if cell_coords:
            if self.board[cell_coords[0]][cell_coords[1]] == -1:
                self.open_cell(cell_coords)

    # метод - диспетчер, который получает событие нажатия и вызывает первые два метода
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def open_cell(self, cell_coords):
        y, x = cell_coords
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= y + i < self.height and 0 <= x + j < self.width:
                    if self.board[y + i][x + j] == 10:
                        count += 1
        self.board[y][x] = count


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Дедушка сапёра')

    board = Minesweeper(10, 15, 15)
    board.set_view(5, 5, 30)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
        screen.fill('black')
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
