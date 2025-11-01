import random
import math
import pygame
pygame.init()


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

        for bomb_coordinats in bombs_list:
            x = bomb_coordinats[0]
            y = bomb_coordinats[1]
            if x > 0 and y > 0 and x < self.__size - 1 and y < self.__size - 1:
                self.__matrix[x-1][y-1].add_bomb_near()
                self.__matrix[x-1][y].add_bomb_near()
                self.__matrix[x-1][y+1].add_bomb_near()
                self.__matrix[x][y-1].add_bomb_near()
                self.__matrix[x][y+1].add_bomb_near()
                self.__matrix[x+1][y-1].add_bomb_near()
                self.__matrix[x+1][y].add_bomb_near()
                self.__matrix[x+1][y+1].add_bomb_near()
            elif x == 0 and y == 0:                                                                         
                self.__matrix[x][y+1].add_bomb_near()
                self.__matrix[x+1][y].add_bomb_near()
                self.__matrix[x+1][y+1].add_bomb_near()
            elif x == 0 and y != 0 and y != self.__size - 1:
                self.__matrix[x][y-1].add_bomb_near()
                self.__matrix[x][y+1].add_bomb_near()
                self.__matrix[x+1][y-1].add_bomb_near()
                self.__matrix[x+1][y].add_bomb_near()
                self.__matrix[x+1][y+1].add_bomb_near()
            elif x == 0 and y == self.__size - 1:
                self.__matrix[x][y-1].add_bomb_near()
                self.__matrix[x+1][y-1].add_bomb_near()
                self.__matrix[x+1][y].add_bomb_near()
            elif x != 0 and x != self.__size - 1 and y == 0:
                self.__matrix[x-1][y].add_bomb_near()
                self.__matrix[x-1][y+1].add_bomb_near()
                self.__matrix[x][y+1].add_bomb_near()
                self.__matrix[x+1][y].add_bomb_near()
                self.__matrix[x+1][y+1].add_bomb_near()
            elif x == self.__size - 1 and y == self.__size - 1:
                self.__matrix[x-1][y-1].add_bomb_near()
                self.__matrix[x-1][y].add_bomb_near()
                self.__matrix[x][y-1].add_bomb_near()
            elif x == self.__size - 1 and y == 0:
                self.__matrix[x-1][y].add_bomb_near()
                self.__matrix[x-1][y+1].add_bomb_near()
                self.__matrix[x][y+1].add_bomb_near()
            elif x == self.__size - 1 and y != 0 and y != self.__size - 1:
                self.__matrix[x-1][y-1].add_bomb_near()
                self.__matrix[x-1][y].add_bomb_near()
                self.__matrix[x-1][y+1].add_bomb_near()
                self.__matrix[x][y-1].add_bomb_near()
                self.__matrix[x][y+1].add_bomb_near()
            elif x != self.__size - 1 and x != 0 and y == self.__size - 1:
                self.__matrix[x-1][y-1].add_bomb_near()
                self.__matrix[x-1][y].add_bomb_near()
                self.__matrix[x][y-1].add_bomb_near()
                self.__matrix[x+1][y-1].add_bomb_near()
                self.__matrix[x+1][y].add_bomb_near()


class Cell:
    TYPE_EMPTY = 0
    TYPE_BOMB = 1

    STATE_CLOSED = 0
    STATE_OPENED = 1
    STATE_FLAGGED = 2

    def __init__(self, type):
        self.__type = type
        self.__state = Cell.STATE_CLOSED
        self.__bombs_near = 0

    @property
    def type(self):
        return self.__type

    @property
    def state(self):
        return self.__state

    @property
    def bombs_near(self):
        return self.__bombs_near

    def __repr__(self):
        if self.__type == 0:
            return f'{self.__bombs_near}'
        return '*'

    def open(self):
        if self.__state != Cell.STATE_FLAGGED:
            self.__state = Cell.STATE_OPENED

    def set_flag(self):
        self.__state = Cell.STATE_FLAGGED

    def add_bomb_near(self):
        self.__bombs_near += 1

    def get_image(self):
        return pygame.image.load(f'items/mine_near_{self.__bombs_near}')

a = Battlefield()
a.restart()
b = a.matrix

for x in range(len(b)):
    for y in range(len(b[x])):  
        print(b[x][y], end=' ')
    print()