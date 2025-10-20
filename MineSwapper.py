import random

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
        self.__bombs_count = self.__size + 1
        self.__matrix = [[Cell(Cell.TYPE_EMPTY) for _ in range(self.__size)] for _ in range(self.__size)]

        self.__bombs_coordinats = []
        self.__attemps = 0
        if self.__attemps < 1000:
            for x in random.randint(0, self.__size):
                for y in random.randint(0, self.__size):
                    if len(self.__bombs_coordinats) != 0:
                        if f'{x},{y}' in self.__bombs_coordinats:
                            continue
                        for z in range(len(self.__bombs_coordinats)):
                            if abs(x - int(self.__bombs_coordinats[z][0])) < 1 and abs(y - int(self.__bombs_coordinats[z][2])) < 1:
                                continue
                    self.__matrix[x][y] = Cell(Cell.TYPE_BOMB)
                    self.__bombs_coordinats.append(f'{x},{y}')
                    self.__bombs_count -= 1


        for x in range(self.__size):
            for y in range(self.__size):
                if f'{x},{y}' not in self.__bombs_coordinats and self.__bombs_count != 0:
                    self.__matrix[x][y] = Cell(Cell.TYPE_BOMB)
                    self.__bombs_count -= 1
        if self.__bombs_count != 0:
            self.__matrix[0][self.__size - 1] = Cell(Cell.TYPE_BOMB)

class Cell:
    TYPE_EMPTY = 0
    TYPE_BOMB = 1

    STATE_FLAGGED = 2
    STATE_OPENED = 1
    STATE_CLOSED = 0

    def __init__(self):
        self.__type = type
        self.__state = Cell.STATE_CLOSED
        self.bombs_around = 0

    @property
    def type(self):
        if self.__type == 0:
            return 'EMPTY'
        return 'BOMB' 

    @property
    def state(self):
        if self.__state == 0:
            return 'CLOSE'
        elif self.__state == 1:
            return 'OPEN'
        return 'FLAG'

    def open(self):
        self.__state = Cell.STATE_OPENED

    def close(self):
        self.__state = Cell.STATE_CLOSED

    def set_flag(self):
        self.__state = Cell.STATE_FLAGGED