from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Выстрел за доску!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку!'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, n, le, d):
        self.n = n
        self.le = le
        self.d = d
        self.life = le

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.le):
            cor_x = self.n.x
            cor_y = self.n.y

            if self.d == 0:
                cor_x += i
            elif self.d == 1:
                cor_y += i

            ship_dots.append(Dot(cor_x, cor_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.field = [['0']*6 for i in range(size)]
        self.ships = []
        self.busy = []
        self.count = 0

    def add_ship(self, ship):
        for d in ship.dots:
            if (self.out(d)) or (d in self.busy):
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [(-1, 1), (0, 1), (1, 1),
                (-1, 0), (0, 0), (1, 0),
                (-1, -1), (0, -1), (1, -1)]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if cur not in self.busy and not self.out(cur):
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    def __str__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | {" | ".join(row)} |'
        if self.hid:
            res = res.replace('■', '0')
        return res

    def out(self, d):
        if (0 <= d.x < 6) and (0 <= d.y < 6):
            return False
        return True

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if ship.shooten(d):
                ship.life -= 1
                self.field[d.x][d.y] = 'X'
                if ship.life == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Убит!')
                    return True
                else:
                    print('Ранен!')
                    return True
        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        # a = Game()
        # n = [(0, 1), (-1, 0), (0, 0), (1, 0), (0, -1)]
        # cords = [(i, j.index('X')) for i, j in enumerate(a.us.board.field) if 'X' in j]
        # for q, w in cords:
        #     cor = Dot(q, w)
        #     for dx, dy in n:
        #         cur = Dot(cor.x + dx, cor.y + dy)
        #         d = cur
        #         print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        #         return d
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input('Введите 2 координаты: ').split()
            if len(cords) != 2:
                print('Введите 2 координаты: ')
                continue

            x, y = cords

            if not x.isdigit() and not y.isdigit():
                print('Введите 2 числа: ')
                continue

            x, y = int(x), int(y)
            return Dot(x-1, y-1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.us = User(pl, co)
        self.ai = AI(co, pl)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts >= 2000:
                    return None
                ship = Ship(Dot(randint(0, 5), randint(0, 5)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    # def show(self):
    #     _N = 0
    #     row0 = '  | 1 | 2 | 3 | 4 | 5 | 6 |'
    #     row3 = row0 + '   ' + row0
    #     print(row3)
    #     print('-' * 27 + '   ' + '-' * 27)
    #     for h, row1 in enumerate(self.us.board):
    #         for k, row2 in enumerate(self.ai.board):
    #             _N += 1
    #             if _N == k + 1 and _N == h + 1:
    #                 row = f'{h + 1} | {" | ".join(row1)} |   {k + 1} | {" | ".join(row2)} |'
    #                 print(row)
    #                 print('-' * 27 + '   ' + '-' * 27)
    #             elif _N == 6:
    #                 _N = 0

    def loop(self):
        num = 0
        while True:
            print('Доска игрока')
            print(self.us.board)
            print('Доска компьютера')
            print(self.ai.board)
            if num % 2 == 0:
                print('Вы ходите!')
                repeat = self.us.move()
            else:
                print('Ходит компьютер!')
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print('Вы выиграли!')
                break
            if self.us.board.count == 7:
                print('Вы проиграли!')
                break
            num += 1

    def greet(self):
        print('Добро пожаловать в игру Морской Бой!')
        print('В игре нужно будет вводить 2 координаты,')
        print('где х - номер столбца, а y - номер строки.')

    def start(self):
        self.greet()
        self.loop()


s = Game()
s.start()


