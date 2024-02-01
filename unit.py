from FC import *


class Unit:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.board = [[[0, -1] for j in range(height)] for i in range(width)]
        self.red_alert = False
        self.moving = False
        self.alerts = None
        self.type = 'wall'
        self.fraction = 'Human'
        self.activated = False
        self.show = False
        self.healing = 0
        self.hp = 0
        self.power = 0
        self.max_hp = 0
        self.had_been_activated_at_this_hod = False  # Легальный чит через фастсейвы(Не баг а фича!)

    def init_unit(self, type):
        self.type = type
        if self.type == 'higth_fleet':
            self.power = 20
            self.hp = 80
            self.max_hp = 80
        elif self.type == 'pehot':
            self.power = 20
            self.hp = 100
            self.max_hp = 100
        elif self.type == 'fleet':
            self.power = 20
            self.hp = 200
            self.max_hp = 200

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                lt = (self.left + self.cell_size * i, self.top + self.cell_size * j)
                rt = (self.left + self.cell_size * (i + 1), self.top + self.cell_size * j)
                rd = (self.left + self.cell_size * (i + 1), self.top + self.cell_size * (j + 1))
                ld = (self.left + self.cell_size * i, self.top + self.cell_size * (j + 1))
                coord = (lt, rt, rd, ld)
                center = (lt[0] + self.cell_size / 2, lt[1] + self.cell_size / 2)
                if self.board[i][j][0] == 2:
                    if self.fraction == 'Human':
                        if self.type == 'higth_fleet':
                            im = pygame.image.load(r'data\sprites\plain.png').convert_alpha()
                            screen.blit(im, (lt, rt))
                        elif self.type == 'pehot':
                            im = pygame.image.load(r'data\sprites\pehot.png').convert_alpha()
                            screen.blit(im, (lt, rt))
                        elif self.type == 'fleet':
                            im = pygame.image.load(r'data\sprites\boat.png').convert_alpha()
                            screen.blit(im, (lt, rt))
                    else:
                        if self.type == 'higth_fleet':
                            im = pygame.image.load(r'data\sprites\inseecf.png').convert_alpha()
                            screen.blit(im, (lt, rt))
                        elif self.type == 'pehot':
                            im = pygame.image.load(r'data\sprites\inseec.png').convert_alpha()
                            screen.blit(im, (lt, rt))
                        elif self.type == 'fleet':
                            im = pygame.image.load(r'data\sprites\inseecw.png').convert_alpha()
                            screen.blit(im, (lt, rt))
                    if self.activated:
                        pygame.draw.polygon(screen, 'Black', coord, 5)
                    if self.max_hp != self.hp:
                        lt = (lt[0] + 10, lt[1] + 30)
                        rd = (20, 5)
                        pygame.draw.rect(screen, (20, 20, 20), (lt, rd))
                        lt = (lt[0] + 1, lt[1] + 1)
                        rd = (int(18 * (self.hp / self.max_hp)), 4)
                        pygame.draw.rect(screen, 'GREEN', (lt, rd))
        if self.activated:
            self.alerts_show = [self.red_alert]
            if self.type == 'fleet':
                ogran = 2
            elif self.type == 'pehot':
                ogran = 1
            elif self.type == 'higth_fleet':
                ogran = 3
            for i in range(ogran):
                for x, y in self.alerts_show.copy():
                    self.open_sosed_for_unit(x, y, i)
            for elem in self.alerts_show:
                i, j = elem
                lt = (self.left + self.cell_size * i + 15, self.top + self.cell_size * j + 15)
                rt = (self.left + self.cell_size * (i + 1) - 15, self.top + self.cell_size * j + 15)
                rd = (self.left + self.cell_size * (i + 1) - 15, self.top + self.cell_size * (j + 1) - 15)
                ld = (self.left + self.cell_size * i + 15, self.top + self.cell_size * (j + 1) - 15)
                coord = (lt, rt, rd, ld)
                center = (lt[0] + self.cell_size / 2, lt[1] + self.cell_size / 2)
                if self.board[i][j][0] == 0:
                    pygame.draw.polygon(screen, 'WHITE', coord)

    def click(self, coord):
        a = (coord[0] - self.left) // self.cell_size
        b = (coord[1] - self.top) // self.cell_size
        if b in range(0, self.height) and a in range(0, self.width):
            return tuple((a, b))
        else:
            return None

    def sharik(self, coord, stat=False):
        pos = self.click(coord)
        if stat:
            pos = coord
        pos = [pos[1], pos[0]]
        if pos and not self.moving and not self.healing:
            if self.red_alert and self.board[pos[0]][pos[1]][0] not in [1, 2]:
                if self.has_path(pos[0], pos[1], self.red_alert[0], self.red_alert[1]):
                    self.moving = True
            elif self.board[pos[0]][pos[1]][0] == 0:
                self.board[pos[0]][pos[1]][0] = 1
            elif self.board[pos[0]][pos[1]][0] == 1 and not self.red_alert:
                self.board[pos[0]][pos[1]][0] = 2
                self.red_alert = pos

    def has_path(self, x1, y1, x2, y2):
        # Сюда не лезьть, я сам не ебу что тут происходит:(
        new_board = []
        for elem in self.board:
            proto = []
            for obj in elem:
                proto.append([obj[0], -1])
            new_board.append(proto)
        ogran = 0
        if self.type == 'fleet':
            ogran = 2
        elif self.type == 'pehot':
            ogran = 1
        elif self.type == 'higth_fleet':
            ogran = 3
        self.board = new_board
        self.board[x1][y1][1] = 0
        self.alerts = [(x1, y1)]
        count = 0
        while len(self.alerts) != len(self.board) * len(self.board) and count < ogran:
            count += 1
            for x, y in self.alerts.copy():
                self.open_sosed(x, y, count)
        if self.board[x2][y2][1] != -1:
            return True
        return False

    def open_sosed(self, x, y, i):
        # Сюда не лезьть, я сам не ебу что тут происходит:(
        alert = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for x, y in alert:
            try:
                if x < 0 or y < 0:
                    raise Exception
                if self.board[x][y][1] == -1 and (self.board[x][y][0] == 0 or self.board[x][y][0] == 2):
                    self.alerts.append((x, y))
                    self.board[x][y][1] = i
            except Exception as e:
                pass

    def min_sosed(self):
        # Сюда не лезьть, я сам не знвю что тут происходит:(
        x, y = self.red_alert
        alert = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        minimal = float('inf')
        coord = [x, y]
        for x, y in alert:
            try:
                if x < 0 or y < 0:
                    raise Exception
                if self.board[x][y][1] != -1 and self.board[x][y][1] < minimal and self.board[x][y][0] not in (1, 2):
                    minimal = self.board[x][y][1]
                    coord = [x, y]
                if minimal == 0:
                    self.moving = False
                    for i in range(len(self.board)):
                        for j in range(len(self.board[i])):
                            self.board[i][j][1] = -1
                    return coord
            except Exception as e:
                pass
        return coord

    def iteration(self):
        # Действия юнита
        self.healing = 0
        pos = self.min_sosed()
        x, y = self.red_alert
        self.board[x][y][0] = 0
        self.board[pos[0]][pos[1]][0] = 2
        self.red_alert = pos
        if not self.moving:
            self.alerts = []

    def copy(self):
        # Смешнявка(любое перемещение юнита это создание нового и замена им старого)
        unit = Unit(self.width, self.height)
        unit.board = [elem.copy() for elem in self.board]
        unit.left = self.left
        unit.top = self.top
        unit.cell_size = self.cell_size
        unit.type = self.type
        unit.fraction = self.fraction
        unit.hp = self.hp
        unit.healing = self.healing
        unit.power = self.power
        unit.had_been_activated_at_this_hod = self.had_been_activated_at_this_hod
        unit.max_hp = self.max_hp
        if self.red_alert:
            unit.red_alert = self.red_alert.copy()
        if self.alerts:
            unit.alerts = self.alerts.copy()
        return unit

    def activate(self):
        # тут понятно
        self.activated = True

    def diactivate(self):
        # тут понятно
        self.activated = False
        self.show = True

    def atributs(self):
        # Система для сейва
        atributs = {
            'board': [elem.copy() for elem in self.board],
            'type': self.type,
            'fraction': self.fraction,
            'hp': self.hp,
            'healing': self.healing,
            'power': self.power,
            'max_hp': self.max_hp
        }
        if self.red_alert:
            atributs['red_alert'] = self.red_alert.copy()
        if self.alerts:
            atributs['alerts'] = self.alerts.copy()
        return atributs

    def heal(self):
        if self.hp < self.max_hp - 10:
            self.hp += 10
        else:
            self.hp = self.max_hp
        self.had_been_activated_at_this_hod = True

    def open_sosed_for_unit(self, x, y, i):
        # Сюда не лезьть, я сам не ебу что тут происходит:(
        alert = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for x, y in alert:
            try:
                if x < 0 or y < 0:
                    raise Exception
                if self.board[x][y][1] == -1 and (self.board[x][y][0] == 0 or self.board[x][y][0] == 2):
                    self.alerts_show.append((x, y))
            except Exception as e:
                pass
