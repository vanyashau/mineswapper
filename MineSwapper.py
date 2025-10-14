import random
import pygame  
pygame.init()  

class EmptyCell:
    """Родительский класс где определяються методы для дочерних"""

    def __init__(self):
        self.opened = False
        self.flagged = False
        self.bombed = False
        self.bombs_around = 0

    def is_open(self):
        return self.opened

    def open(self):
        self.opened = True

    def toggle_flag(self):
        self.flagged = not self.flagged

    def is_bomb(self):
        return False
    
    def add_bomb_around(self):
        self.bombs_around += 1

class BorderCell(EmptyCell):
    """Класс клетки граничущей с бомбами"""
    def __init__(self, bombs_around):
        super().__init__()
        self.bombs_around = bombs_around

class SafetyCell(EmptyCell):
    """Класс клетки неграничющей с бомбой и ею не являющейся"""
    def __init__(self):
        super().__init__()

class BombCell(EmptyCell):
    """Класс непосредственно бомбы"""
    def is_bomb(self):
        return True
    
def create_matrix(side):
    count_of_bombs = side + 1
    matrix = [[False for _ in range(side)] for _ in range(side)]
    coordinats = []
    attempts = 0

    while len(coordinats) < count_of_bombs and attempts < 1000:
        x = random.randint(0, side - 1)
        y = random.randint(0, side - 1)

        if (x, y) in coordinats:
            attempts += 1
            continue

        too_close = False
        for selested_x, selested_y in coordinats:
            if abs(x - selested_x) <= 1 and abs(y - selested_y) <= 1:
                too_close = True
                break

        if too_close:
            attempts += 1
            continue

        coordinats.append((x, y))
        matrix[x][y] = True
        attempts = 0

    while len(coordinats) < count_of_bombs:
        x = random.randint(0, side - 1)
        y = random.randint(0, side - 1)
        if (x, y) not in coordinats:
            coordinats.append((x, y))
            matrix[x][y] = True
    return matrix

def create_field(matrix, side):
    for x in range(side):
        for y in range(side):
            if matrix[x][y]:
                matrix[x][y] = BombCell()
            else:
                matrix[x][y] = EmptyCell()

    for x in range(side):
        for y in range(side):
            if matrix[x][y].is_bomb():
                if x > 0 and y > 0 and x < 9 and y < 9:
                    matrix[x-1][y-1].add_bomb_around()
                    matrix[x-1][y].add_bomb_around()
                    matrix[x-1][y+1].add_bomb_around()
                    matrix[x][y-1].add_bomb_around()
                    matrix[x][y+1].add_bomb_around()
                    matrix[x+1][y-1].add_bomb_around()
                    matrix[x+1][y].add_bomb_around()
                    matrix[x+1][y+1].add_bomb_around()
                elif x == 0 and y == 0:                                                                         
                    matrix[x][y+1].add_bomb_around()
                    matrix[x+1][y].add_bomb_around()
                    matrix[x+1][y+1].add_bomb_around()
                elif x == 0 and y != 0 and y != 9:
                    matrix[x][y-1].add_bomb_around()
                    matrix[x][y+1].add_bomb_around()
                    matrix[x+1][y-1].add_bomb_around()
                    matrix[x+1][y].add_bomb_around()
                    matrix[x+1][y+1].add_bomb_around()
                elif x == 0 and y == 9:
                    matrix[x][y-1].add_bomb_around()
                    matrix[x+1][y-1].add_bomb_around()
                    matrix[x+1][y].add_bomb_around()
                elif x != 0 and x != 9 and y == 0:
                    matrix[x-1][y].add_bomb_around()
                    matrix[x-1][y+1].add_bomb_around()
                    matrix[x][y+1].add_bomb_around()
                    matrix[x+1][y].add_bomb_around()
                    matrix[x+1][y+1].add_bomb_around()
                elif x == 9 and y == 9:
                    matrix[x-1][y-1].add_bomb_around()
                    matrix[x-1][y].add_bomb_around()
                    matrix[x][y-1].add_bomb_around()
                elif x == 9 and y == 0:
                    matrix[x-1][y].add_bomb_around()
                    matrix[x-1][y+1].add_bomb_around()
                    matrix[x][y+1].add_bomb_around()
                elif x == 9 and y != 0 and y != 9:
                    matrix[x-1][y-1].add_bomb_around()
                    matrix[x-1][y].add_bomb_around()
                    matrix[x-1][y+1].add_bomb_around()
                    matrix[x][y-1].add_bomb_around()
                    matrix[x][y+1].add_bomb_around()
                elif x != 9 and x != 0 and y == 9:
                    matrix[x-1][y-1].add_bomb_around()
                    matrix[x-1][y].add_bomb_around()
                    matrix[x][y-1].add_bomb_around()
                    matrix[x+1][y-1].add_bomb_around()
                    matrix[x+1][y].add_bomb_around()
    return matrix