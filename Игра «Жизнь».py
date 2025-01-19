import pygame

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400
FPS = 30


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[1] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        color = pygame.Color(255, 255, 255)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, color, (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                                 self.cell_size, self.cell_size), self.board[y][x])

    #  метод возвращает координаты клетки
    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[1] < self.left + self.height * self.cell_size and \
                self.top <= mouse_pos[0] < self.top + self.width * self.cell_size:
            return (int((mouse_pos[1] - self.left) / self.cell_size), int((mouse_pos[0] - self.top) / self.cell_size))
        else:
            return None

    # метод изменяет поле, опираясь на полученные координаты клетки
    def on_click(self, cell_coords):
        if cell_coords:
            for x in range(self.height):
                self.board[x][cell_coords[1]] = int(not (self.board[x][cell_coords[1]]))
            for y in range(self.width):
                self.board[cell_coords[0]][y] = int(not (self.board[cell_coords[0]][y]))
            self.board[cell_coords[0]][cell_coords[1]] = int(not (self.board[cell_coords[0]][cell_coords[1]]))
            # print(self.board)

    # метод - диспетчер, который получает событие нажатия и вызывает первые два метода
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Чёрное в белое и наоборот')

    board = Board(5, 7)
    # board.set_view(100, 100, 50)

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
