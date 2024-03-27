import keyboard as kb
import colorama


BACK_COLOR = colorama.Fore.GREEN
PACMAN_COLOR = colorama.Fore.WHITE
ENEMY_COLOR1 = colorama.Fore.LIGHTMAGENTA_EX


class Board:
    def __init__(self):
        self.cells = []
        for i in range(25):
            line = []
            for j in range(25):
                line.append('·')
            self.cells.append(line)

    def draw(self):
        print(BACK_COLOR)
        for line in self.cells:
            print(*line)    # распаковываем элементы списка в print

    def build_walls(self):
        self.add_square(5,5)
        self.add_square(19,5)
        self.add_square(5, 19)
        self.add_square(19, 19)


    def add_square(self, center_x, center_y):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                self.cells[center_x + x][center_y + y] = '■'


class Character:
    def __init__(self, x, y, image, direction):
        self.__y = y
        # защищенный атрибут(убирает подсказки)
        # self._x = x
        # приватный атрибут
        self.__x = x
        self.image = image
        self.direction = direction

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def move(self, board: Board):
        # убираем пакмана с текущей клетки
        board.cells[self.__y][self.__x] = '·'
        # двигаем пакмана в зависимости от направления
        if self.direction == 'right' and (self.__x == 24 or board.cells[self.__y][self.__x + 1] != '■'):
            self.__x += 1
            if self.__x == 25:
                self.__x = 0
        elif self.direction == 'left' and (self.__x == 0 or board.cells[self.__y][self.__x - 1] != '■'):
            self.__x -= 1
            if self.__x == -1:
                self.__x = 24
        elif self.direction == 'down' and (self.__y == 24 or board.cells[self.__y + 1][self.__x] != '■'):
            self.__y += 1
            if self.__y == 25:
                self.__y = 0
        elif self.direction == 'up' and (self.__y == 0 or board.cells[self.__y - 1][self.__x] != '■'):
            self.__y -= 1
            if self.__y == -1:
                self.__y = 24
        # ставим пакмана на новую клетку
        board.cells[self.__y][self.__x] = self.image


class PacMan(Character):
    # меняет направление при нажатии на клавишу
    def change_direction(self):
        if kb.is_pressed('w'):
            self.direction = 'up'
        elif kb.is_pressed('a'):
            self.direction = 'left'
        elif kb.is_pressed('s'):
            self.direction = 'down'
        elif kb.is_pressed('d'):
            self.direction = 'right'

    def update(self, board: Board):
        self.change_direction()
        self.move(board)


class Enemy(Character):
    def follow(self, hero: PacMan):
        if self.get_x() < hero.get_x():
            self.direction = 'right'
        elif self.get_x() > hero.get_x():
            self.direction = 'left'
        else:
            # тогда мы находимся в одном столбике
            if self.get_y() < hero.get_y():
                self.direction = 'down'
            elif self.get_y() > hero.get_y():
                self.direction = 'up'

    def update(self, board: Board, hero: PacMan):
        self.follow(hero)
        # если идут не на другого врага
        if self.direction == 'right' and (self.get_x() == 24 or board.cells[self.get_y()][self.get_x() + 1] not in '@+=%') or self.direction == 'left' and (self.get_x() == 0 or board.cells[self.get_y()][self.get_x() - 1] not in '@+=%') or self.direction == 'up' and (self.get_y() == 0 or board.cells[self.get_y() - 1][self.get_x()] not in '@+=%') or self.direction == 'down' and (self.get_y() == 24 or board.cells[self.get_y() + 1][self.get_x()] not in '@+=%'):
            self.move(board)

    def catch_hero(self, hero: PacMan) -> bool:
        return self.get_x() == hero.get_x() and self.get_y() == hero.get_y()
        # if self.x == hero.x and self.y == hero.y:
        #     return True
        # else:
        #     return False
