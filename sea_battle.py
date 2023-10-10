import random

# ВНУТРЕННЯЯ ЛОГИКА

class BoardOutException(Exception):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length, nose, orientation, health):
        self.length = length            #длина корабля
        self.nose = nose                #точка носа корабля
        self.orientation = orientation  #положение корабля в пространстве
        self.health = health            #здоровье корабля

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            if self.orientation == "v":
                dot = Dot(self.nose.x, self.nose.y + i)
            else:
                dot = Dot(self.nose.x + i, self.nose.y)
            ship_dots.append(dot)
        return ship_dots

class Board:
    def __init__(self, hid = False):
        self.field = [['0'] * 6 for _ in range(6)]
        self.list_ship = []
        self.hid = hid
        self.quantity_live_ship = 0
        self.all_ship_dots = []
        self.count = 0

    def add_ship(self, ship: Ship):
        for dot in ship.dots():                                 # цикл проверки выхода точек за пределы доски
            if self.out(dot) or dot in self.all_ship_dots:      # и проверка наличия точек в all_ship_dots
                raise BoardOutException()

        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
            self.all_ship_dots.append(dot)

        self.list_ship.append(ship)
        self.contour(ship)
        self.quantity_live_ship += 1

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots():
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not (self.out(cur) or cur in self.all_ship_dots):
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.all_ship_dots.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | {' | '.join(row)} |"
        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, dot):
        return not ((0 <= dot.x <= 5) and (0 <= dot.y <= 5))
        # для точки (объекта класса Dot) возвращает True если точка выходит за пределы
        # поля, и False, если не выходит
    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.all_ship_dots:
            raise BoardOutException()

        self.all_ship_dots.append(dot)

        for ship in self.list_ship:
            if dot in ship.dots():
                ship.health -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.health == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

# ВНЕШНЯЯ ЛОГИКА

class Player:
    def __init__(self, board, opponent_board):
        self.board = board
        self.opponent_board = opponent_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.opponent_board.shot(target)
                return repeat
            except BoardOutException:
                print("Вы совершили выстрел по занятой точке! Повторите попытку.")
            except Exception as e:
                print(e)

class User(Player):
    def ask(self):
        while True:
            try:
                x, y = map(int, input("Введите координаты выстрела через пробел: ").split())
                x -= 1
                y -= 1
                if 0 <= x < 6 and 0 <= y < 6:
                    return Dot(x, y)
                print("Вводите координаты от 1 до 6!")
            except ValueError:
                print("Вводить можно только числа!")


class AI(Player):
    def ask(self):
        return Dot(random.randint(0, 5), random.randint(0, 5))

class Game:
    def __init__(self):
        my_board = Board()
        other_board = Board(hid=True)
        self.us = User(my_board, other_board)
        self.ai = AI(other_board, my_board)

    def random_board(self, board):
        num = [3, 2, 2, 1, 1, 1, 1]
        t = 0
        for i in num:
            ship = Ship(3, Dot(0, 0), '', 3)
            tf = True
            while tf:
                ship.length = i
                ship.health = i
                ship.nose = Dot(random.randint(0, 5), random.randint(0, 5))
                if random.randint(0, 1) == 0:
                    ship.orientation = 'v'
                else:
                    ship.orientation = 'g'
                try:
                    board.add_ship(ship)
                    tf = False
                except BoardOutException:
                    tf = True
                    t += 1
                    if t > 12000:
                        tf = False

    def greet(self):
        print("-------------------------------------------------")
        print("----- Добро пожаловать в игру Морской бой -------")
        print("Для того, чтобы совершить выстрел вам необходимо")
        print("ввести координаты через пробел, (например 2 6).")
        print("Первое число отвечает за выбор строки, а второе")
        print("за столбец. Вводить можно только цифры от 1 до 6.")
        print("-------------------------------------------------")

    def loop(self):
        num = 0

        while True:
            print("Доска User:")
            print(self.us.board)
            print('-' * 27)
            print("Доска AI:")
            print(self.ai.board)
            print('-' * 27)
            if num % 2 == 0:
                print('-' * 25)
                print("Ход User:")
                repeat = self.us.move()
            else:
                print('-' * 25)
                print("Ход Ai:")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("-" * 25)
                print("Игрок победил!")
                break
            if self.us.board.count == 7:
                print("-" * 25)
                print("Компьютер победил!")
                break
            num += 1

    def start(self):
        while True:
            self.random_board(self.us.board)
            if self.us.board.quantity_live_ship == 7:
                self.us.board.all_ship_dots = []
                break
            else:
                self.us.board.list_ship = []
                self.us.board.all_ship_dots = []
                self.us.board.quantity_live_ship = 0
                self.us.board.field = [['0'] * 6 for _ in range(6)]
                continue
        while True:
            self.random_board(self.ai.board)
            if self.ai.board.quantity_live_ship == 7:
                self.ai.board.all_ship_dots = []
                break
            else:
                self.ai.board.list_ship = []
                self.ai.board.all_ship_dots = []
                self.ai.board.quantity_live_ship = 0
                self.ai.board.field = [['0'] * 6 for _ in range(6)]
                continue
        star.greet()
        star.loop()

if __name__ == '__main__':
    star = Game()
    star.start()
