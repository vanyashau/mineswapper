import pygame  
pygame.init()  

class EmptyCell:
    def __init__(self):
        self.is_opened = False
        self.is_flagged = False

    def open(self):
        self.is_opened = True

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged

    def is_bomb(self):
        return False


class BorderCell(EmptyCell):
    def __init__(self, bombs_around: int):
        super().__init__()
        self.bombs_around = bombs_around


class SafetyCell(EmptyCell):
    def __init__(self):
        super().__init__()
        self.safe = True


class BombCell(EmptyCell):
    def is_bomb(self):
        return True