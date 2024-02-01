from FC import *



class IN:
    def __init__(self, coord, left, top, cell_size, screen):
        self.fraction = 'Inseec'
        self.lvl = 1
        self.type = 'IN'
        self.activated = False
        self.procces = None
        self.position = coord
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.screen = screen
        # cop - coef_of_price
        self.cop = 1
        self.hp = 100
        self.max_hp = 100
        self.price_list = {'pehot': 100 * self.cop, 'fleet': 200 * self.cop, 'higth_fleet': 300 * self.cop}
        self.unit_list = {'pehot': 2, 'fleet': 4, 'higth_fleet': 5}

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        i, j = self.position
        i -= 1
        j -= 1
        lt = (self.cell_size * i, self.cell_size * j)
        rt = (self.cell_size * (i + 1), self.cell_size * j)
        rd = (self.cell_size * (i + 1), self.cell_size * (j + 1))
        ld = (self.cell_size * i, self.cell_size * (j + 1))
        coord = (lt, rt, rd, ld)
        im = pygame.image.load(r'data\sprites\nest.png').convert_alpha()
        center = (lt[0] + self.cell_size / 2, lt[1] + self.cell_size / 2)
        self.screen.blit(im, (lt, rt))
        if self.activated:
            pygame.draw.polygon(self.screen, 'Black', coord, 5)
        if self.max_hp != self.hp:
            lt = (lt[0] + 10, lt[1] + 30)
            rd = (20, 5)
            pygame.draw.rect(self.screen, (20, 20, 20), (lt, rd))
            lt = (lt[0] + 1, lt[1] + 1)
            rd = (int(18 * (self.hp / self.max_hp)), 4)
            pygame.draw.rect(self.screen, 'GREEN', (lt, rd))

    def look_around(self, board, type):
        x, y = self.position
        alert = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for y, x in alert:
            try:
                if x < 1 or y < 1:
                    raise Exception
                if board.board[x][y] == 0 and type != 'fleet':
                    return x, y
                elif board.board[x][y] == 1 and type == 'fleet':
                    return x, y
            except Exception as e:
                pass

    def new_unit(self, board, type, player):
        self.price_list = {'pehot': 100 * self.cop, 'fleet': 200 * self.cop, 'higth_fleet': 300 * self.cop}
        self.unit_list = {'pehot': 2, 'fleet': 4, 'higth_fleet': 5}
        place = self.look_around(board, type)
        if place and type and not self.procces:
            if player.resuorce - self.price_list[type] >= 0:
                self.procces = 2
                player.resuorce -= self.price_list[type]
                self.data_for_unit = (place, type)

    def iteration(self, board, player):
        if self.procces == 1:
            self.lvl += 1
            self.max_hp = self.lvl * 50 + 100
            self.hp = self.max_hp
            self.cop -= self.lvl * 0.1
        elif self.procces == 2:
            place = self.data_for_unit[0]
            board.board[place[0]][place[1]] = self.unit_list[self.data_for_unit[1]]
            if self.data_for_unit[1] == 'higth_fleet':
                unit = board.rock_unit_wall.copy()
            elif self.data_for_unit[1] == 'fleet':
                unit = board.earth_unit_wall.copy()
            else:
                unit = board.water_unit_wall.copy()
            unit.red_alert = [place[1], place[0]]
            unit.fraction = 'Inseec'
            unit.board[place[1]][place[0]] = [2, -1]
            unit.init_unit(self.data_for_unit[1])
            board.units['unit' + str(len(board.units))] = unit
            board.alerts += 1
            self.data_for_unit = None
        self.procces = None
        player.resuorce += 40
        if self.hp + 15 < self.max_hp:
            self.hp += 15
        else:
            self.hp = self.max_hp

    def lvl_up(self, player):
        if player.resuorce - self.lvl * 50 - 150 >= 0 and self.lvl != 3 and not self.procces:
            player.resuorce -= self.lvl * 50 + 150
            self.procces = 1

    def activate(self):
        self.activated = True

    def diactivate(self):
        self.activated = False

    def atributs(self):
        # Система для сейва
        atributs = {
            'type': 'IN',
            'cell_size': self.cell_size,
            'hp': self.hp,
            'lvl': self.lvl,
            'cop': self.cop,
            'position': self.position,
            'max_hp': self.max_hp
        }
        return atributs
