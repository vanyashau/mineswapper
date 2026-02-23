import random
import math
import pygame
pygame.init()

MIN_SIDE_LENGHT = 5
MAX_SIDE_LENGHT = 10

def field_opener(scene ,matrix, size, side, x, y, interface_line, opened_coordinats):
    cell = matrix[x][y]
    
    if cell.type == Cell.TYPE_BOMB:
        return opened_coordinats

    cell.open()
    scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))

    if cell.bombs_around > 0:
        return opened_coordinats
    

    if x - 1 >= 0 and y - 1 >= 0 and f'{x-1},{y-1}' not in opened_coordinats:
        cell = matrix[x-1][y-1]
        opened_coordinats.append(f'{x-1},{y-1}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x-1, y-1, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    if x - 1 >= 0 and f'{x-1},{y}' not in opened_coordinats:
        cell = matrix[x-1][y]
        opened_coordinats.append(f'{x-1},{y}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x-1, y, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    if x - 1 >= 0 and y + 1 < size and f'{x-1},{y+1}' not in opened_coordinats:
        cell = matrix[x-1][y+1]
        opened_coordinats.append(f'{x-1},{y+1}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x-1, y+1, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    if y - 1 >= 0 and f'{x},{y-1}' not in opened_coordinats:
        cell = matrix[x][y-1]
        opened_coordinats.append(f'{x},{y-1}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x, y-1, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    if y + 1 < size and f'{x},{y+1}' not in opened_coordinats:
        cell = matrix[x][y+1]
        opened_coordinats.append(f'{x},{y+1}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x, y+1, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    if x + 1 < size and y - 1 >= 0 and f'{x+1},{y-1}' not in opened_coordinats:
        cell = matrix[x+1][y-1]
        opened_coordinats.append(f'{x+1},{y-1}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x+1, y-1, interface_line, opened_coordinats)

    if x + 1 < size and f'{x+1},{y}' not in opened_coordinats:
        cell = matrix[x+1][y]
        opened_coordinats.append(f'{x+1},{y}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x+1, y, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    if x + 1 < size and y + 1 < size and f'{x+1},{y+1}' not in opened_coordinats:
        cell = matrix[x+1][y+1]
        opened_coordinats.append(f'{x+1},{y+1}')
        scene.blit(pygame.transform.scale(cell.get_image(), (side, side)), (side * x, side * y + interface_line))
        fo = field_opener(scene ,matrix, size, side, x+1, y+1, interface_line, opened_coordinats)
        opened_coordinats.extend(fo)

    return opened_coordinats


def draw_field(scene, size, side, interface_line):
    for x in range(size):
        for y in range(size):
            image = pygame.transform.scale(pygame.image.load('items/close_cell.png'), (side, side))
            scene.blit(image, (side * x, side * y + interface_line))
    pygame.display.update()

class Battlefield:
    def __init__(self, min_side=5, max_side=10):
        self.__matrix = None
        self.__size_limits = [min_side, max_side]
        self.__size = 0
        self.__bombs_count = 0

    @property
    def matrix(self):
        return self.__matrix

    @property
    def size(self):
        return self.__size

    @property
    def bombs_count(self):
        return self.__bombs_count

    def restart(self):
        '''Создание матрицы случайного размера от min_side до max_side'''
        self.__matrix = None
        self.__size = random.randint(self.__size_limits[0], self.__size_limits[1])
        self.__bombs_count =  math.floor(self.__size**2 * 0.18)
        self.__matrix = [[Cell(Cell.TYPE_EMPTY) for _ in range(self.__size)] for _ in range(self.__size)]

        bombs_list = []
        bombs_to_place = self.__bombs_count

        failed_attemps = 0
        while failed_attemps < 1000 and bombs_to_place > 0:
            x = random.randint(0, self.__size - 1)
            y = random.randint(0, self.__size - 1)
            if self.__matrix[x][y].type == Cell.TYPE_BOMB:
                failed_attemps += 1
                continue
            self.__matrix[x][y] = Cell(Cell.TYPE_BOMB)
            bombs_list.append([x, y])
            if x - 1 >= 0 and x - 1 <= self.__size - 1 and y - 1 >= 0 and y - 1 <= self.__size - 1:
                self.__matrix[x-1][y-1].increase_bomb_around()

            if x - 1 >= 0 and x - 1 <= self.__size - 1 and y >= 0 and y <= self.__size - 1:
                self.__matrix[x-1][y].increase_bomb_around()

            if x - 1 >= 0 and x - 1 <= self.__size - 1 and y + 1 >= 0 and y + 1 <= self.__size - 1:
                self.__matrix[x-1][y+1].increase_bomb_around()

            if x >= 0 and x <= self.__size - 1 and y - 1 >= 0 and y - 1 <= self.__size - 1:
                self.__matrix[x][y-1].increase_bomb_around()

            if x >= 0 and x <= self.__size - 1 and y + 1 >= 0 and y + 1 <= self.__size - 1:
                self.__matrix[x][y+1].increase_bomb_around()

            if x + 1 >= 0 and x + 1 <= self.__size - 1 and y - 1 >= 0 and y - 1 <= self.__size - 1:
                self.__matrix[x+1][y-1].increase_bomb_around()

            if x + 1 >= 0 and x + 1 <= self.__size - 1 and y >= 0 and y <= self.__size - 1:
                self.__matrix[x+1][y].increase_bomb_around()
            
            if x + 1 >= 0 and x + 1 <= self.__size - 1 and y + 1 >= 0 and y + 1 <= self.__size - 1:
                self.__matrix[x+1][y+1].increase_bomb_around()

            bombs_to_place -= 1

        if bombs_to_place > 0:
            for x in range(self.__size):
                for y in range(self.__size):
                    if self.__matrix[x][y].type == Cell.TYPE_EMPTY and bombs_to_place > 0:
                        self.__matrix[x][y] = Cell(Cell.TYPE_BOMB)
                        bombs_list.append([x, y])
                        bombs_to_place -= 1
                        if bombs_to_place == 0:
                            break
                if bombs_to_place == 0:
                    break


class Cell:
    TYPE_EMPTY = 0
    TYPE_BOMB = 1

    STATE_CLOSED = 0
    STATE_OPENED = 1
    STATE_FLAGGED = 2

    def __init__(self, type):
        self.__type = type
        self.__state = Cell.STATE_CLOSED
        self.__bombs_around = 0

    @property
    def type(self):
        return self.__type

    @property
    def state(self):
        return self.__state

    @property
    def bombs_around(self):
        return self.__bombs_around

    def __repr__(self):
        if self.__type == 0:
            return f'{self.__bombs_around}'
        return '*'

    def open(self):
        if self.__state != Cell.STATE_FLAGGED:
            self.__state = Cell.STATE_OPENED

    def set_flag(self):
        self.__state = Cell.STATE_FLAGGED

    def increase_bomb_around(self):
        self.__bombs_around += 1

    def get_image(self):
        if self.type == Cell.TYPE_EMPTY:
            return pygame.image.load(f'items/mine_near_{self.__bombs_around}.png')
        elif self.state == Cell.STATE_FLAGGED:
            return pygame.image.load('items/decoy_mine.png')
        return pygame.image.load('items/open_mine.png')


a = Battlefield()
a.restart()
matrix = a.matrix

size = a.size


INTERFACE_LINE = 150
WINDOW_WIDTH = 640
WINDOW_HEIGHT = WINDOW_WIDTH + INTERFACE_LINE

side = WINDOW_WIDTH // size

sc = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f'Mineswapper, size - {size}')
pygame.display.set_icon(pygame.image.load('items/flag_cell.png'))
draw_field(sc ,int(size), side, INTERFACE_LINE)

bombs_to_place = a.bombs_count
FPS = 10
clock = pygame.time.Clock()
game_won = False
mouse_X, mouse_Y = 0, 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_X, mouse_Y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                X_quad = int(mouse_X) // side
                Y_quad = (int(mouse_Y) - INTERFACE_LINE) // side
                matrix[X_quad][Y_quad].open()
                if matrix[X_quad][Y_quad].type == Cell.TYPE_BOMB:
                    game_won = True
                    sc.blit(pygame.transform.scale(pygame.image.load('items/expld_mine.png'),(side, side)), (side * X_quad, side * Y_quad  + INTERFACE_LINE))
                    for x in range(a.size):
                        for y in range(a.size):
                            if x != X_quad or y != Y_quad:
                                sc.blit(pygame.transform.scale(matrix[x][y].get_image(),(side, side)), (side * x, side * y  + INTERFACE_LINE))
                if matrix[X_quad][Y_quad].type == Cell.TYPE_EMPTY:
                    field_opener(sc ,matrix, a.size, side, X_quad, Y_quad, INTERFACE_LINE, [])
    pygame.display.update()
    clock.tick(FPS)