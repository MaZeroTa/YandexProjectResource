from FC import *
from city import City
from resource_station import RS
from inseec_nest import IN
from player import Player
from unit import Unit


class Board:
    def __init__(self, width, height, filename, screen):
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.board = readmap(filename)
        self.board_clever = readmap(filename, True)
        self.water_unit_wall = Unit(width, height)
        self.water_unit_wall.set_view(10, 10, 30)
        self.rock_unit_wall = Unit(width, height)
        self.rock_unit_wall.set_view(10, 10, 30)
        self.earth_unit_wall = Unit(width, height)
        self.earth_unit_wall.set_view(10, 10, 30)
        self.units = dict()
        self.alerts = sum([elem.count(2) + elem.count(4) + elem.count(5) for elem in self.board])
        self.active = None
        self.screen = screen
        self.walls_ready = False
        self.hod = 'Human'
        self.human_alerts = 0
        self.inseec_alerts = 0
        self.bildings_alerts = sum([elem.count(6) + elem.count(7) + elem.count(8) for elem in self.board])
        self.alerts_inseec_nest = 1
        self.alerts_city = 1
        self.bildings = dict()
        self.players = {'Human': Player(), 'Inseec': Player()}
        self.menu = None
        self.ab = None
        self.screen.fill('BLACK')
        self.render()
        self.bilder = []
        self.dead_human = 0
        self.destroid_city = 0
        self.destroid_nests = 0
        self.dead_inseec = 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.water_unit_wall.set_view(left, top, cell_size)
        self.rock_unit_wall.set_view(left, top, cell_size)
        self.earth_unit_wall.set_view(left, top, cell_size)

    def render(self):
        self.menu = None
        screen = self.screen
        cletka = self.cell_size
        for i in range(self.width):
            for j in range(self.height):
                lt = (self.left + cletka * i, self.top + cletka * j)
                rt = (self.left + cletka * (i + 1), self.top + cletka * j)
                rd = (self.left + cletka * (i + 1), self.top + cletka * (j + 1))
                ld = (self.left + cletka * i, self.top + cletka * (j + 1))
                coord = (lt, rt, rd, ld)
                try:
                    if j == 0 or i == 0 or i == self.width - 1 or j == self.height - 1:
                        self.water_unit_wall.board[i][j] = [1, -1]
                        self.rock_unit_wall.board[i][j] = [1, -1]
                        self.earth_unit_wall.board[i][j] = [1, -1]
                    if self.board_clever[j][i] == 1 or self.board_clever[j][i] == 4:
                        self.water_unit_wall.board[i][j] = [1, -1]
                        im = pygame.image.load(r'data\sprites\water.png').convert_alpha()
                        screen.blit(im, (lt, rt))
                        if i == self.width - 1 and j == self.height - 1:
                            self.walls_ready = True
                    elif self.board_clever[j][i] == 3:
                        self.rock_unit_wall.board[i][j] = [1, -1]
                        self.earth_unit_wall.board[i][j] = [1, -1]
                        im = pygame.image.load(r'data\sprites\mountain.png').convert_alpha()
                        screen.blit(im, (lt, rt))
                    elif self.board_clever[j][i] == 0 or self.board_clever[j][i] == 2 or self.board_clever[j][i] == 5:
                        im = pygame.image.load(r'data\sprites\grass.png').convert_alpha()
                        screen.blit(im, (lt, rt))
                    if self.board[j][i] == 2 and len(self.units) < self.alerts and self.walls_ready:
                        if not self.position_of_unit((j, i)):
                            unit = self.water_unit_wall.copy()
                            unit.init_unit('pehot')
                            unit.board[i][j] = [2, -1]
                            unit.red_alert = [i, j]
                            unit.render(screen)
                            self.units['unit' + str(len(self.units))] = unit
                    elif self.board[j][i] == 4 and len(self.units) < self.alerts and self.walls_ready:
                        if not self.position_of_unit((j, i)):
                            unit = self.earth_unit_wall.copy()
                            unit.init_unit('fleet')
                            unit.board[i][j] = [2, -1]
                            unit.red_alert = [i, j]
                            unit.render(screen)
                            self.units['unit' + str(len(self.units))] = unit
                    elif self.board[j][i] == 5 and len(self.units) < self.alerts and self.walls_ready:
                        if not self.position_of_unit((j, i)):
                            unit = self.rock_unit_wall.copy()
                            unit.init_unit('higth_fleet')
                            unit.board[i][j] = [2, -1]
                            unit.red_alert = [i, j]
                            unit.render(screen)
                            self.units['unit' + str(len(self.units))] = unit
                    if self.board[j][i] == 6 and len(self.bildings) < self.bildings_alerts:
                        if not self.position_of_bilding((j, i)):
                            city = City((i, j), self.left, self.top, self.cell_size, screen)
                            city.set_view(self.left, self.top, 40)
                            self.bildings['bilding' + str(len(self.bildings))] = city
                            city.render()
                    elif self.board[j][i] == 7 and len(self.bildings) < self.bildings_alerts:
                        if not self.position_of_bilding((j, i)):
                            rs = RS((i, j), self.left, self.top, self.cell_size, screen)
                            rs.set_view(self.left, self.top, 40)
                            self.bildings['bilding' + str(len(self.bildings))] = rs
                            rs.render()
                    elif self.board[j][i] == 8 and len(self.bildings) < self.bildings_alerts:
                        if not self.position_of_bilding((j, i)):
                            inseec_nest = IN((i, j), self.left, self.top, self.cell_size, screen)
                            inseec_nest.set_view(self.left, self.top, 40)
                            self.bildings['bilding' + str(len(self.bildings))] = inseec_nest
                            inseec_nest.render()
                    if self.board[j][i] in [3, 0, 2]:
                        self.earth_unit_wall.board[i][j] = [1, -1]
                except:
                    print()
                    pass
        for elem in self.units:
            self.units[elem].render(screen)
            if self.units[elem].activated:
                self.menu = self.units[elem].type
        for elem in self.bildings:
            self.bildings[elem].render()
            if self.bildings[elem].activated:
                self.menu = self.bildings[elem].type
        rdd = (rd[0], rt[1] + cletka * 5)
        ltd = (self.left, lt[1])
        ldd = (self.left, lt[1] + cletka * 5)
        pygame.draw.polygon(screen, (50, 50, 50), (ldd, ltd, rt, rdd))
        coords = ((1700, 900), (1900, 900), (1900, 960), (1700, 960))
        pygame.draw.polygon(screen, (20, 20, 20), coords)
        coords = ((1700, 990), (1900, 990), (1900, 1050), (1700, 1050))
        pygame.draw.polygon(screen, (20, 20, 20), coords)
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(int(self.players['Human'].resuorce)), True, 'WHITE')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (1800, 915)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(int(self.players['Inseec'].resuorce)), True, 'WHITE')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (1800, 1005)
        screen.blit(text_surface, text_rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.hod, True, 'WHITE')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (1800, 1055)
        screen.blit(text_surface, text_rect)
        if self.menu:
            coords = ((10, 900), (560, 900), (560, 1060), (10, 1060))
            pygame.draw.polygon(screen, (20, 20, 20), coords)
            coords = ((570, 900), (1120, 900), (1120, 1060), (570, 1060))
            pygame.draw.polygon(screen, (20, 20, 20), coords)
        font = pygame.font.Font(None, 80)
        if self.menu in ('City', 'IN'):
            text_surface = font.render('НОВЫЙ ЮНИТ', True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (840, 955)
            screen.blit(text_surface, text_rect)
            text_surface = font.render('НОВЫЙ УРОВЕНЬ', True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (280, 920)
            screen.blit(text_surface, text_rect)
            text_surface = font.render(f'{int(self.bildings[self.ab].lvl * 50 + 150)}', True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (280, 980)
            screen.blit(text_surface, text_rect)
            text_surface = font.render('Уровень города: ' + str(int(self.bildings[self.ab].lvl)), True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (1400, 900)
            screen.blit(text_surface, text_rect)
            text_surface = font.render('Здоровье: ' + str(int(self.bildings[self.ab].hp)), True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (1400, 970)
            screen.blit(text_surface, text_rect)
        elif self.menu in ('pehot', 'fleet', 'higth_fleet'):
            text_surface = font.render('ПОСТРОИТЬ', True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (840, 955)
            screen.blit(text_surface, text_rect)
            text_surface = font.render('ВОССТАНОВИТЬСЯ', True, 'WHITE')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (285, 955)
            screen.blit(text_surface, text_rect)

    def click(self, coord, stat=False):
        # Я распеределил соотношения по типу камень ножницы бумага (флот авиация пехота)
        # 0.1 - преимущество атаки
        attack_unit = {'pehot_to_higth_fleet': 0.6,
                       'pehot_to_fleet': 1.6,
                       'pehot_to_pehot': 1.1,
                       'higth_fleet_to_pehot': 1.6,
                       'higth_fleet_to_fleet': 0.6,
                       'higth_fleet_to_higth_fleet': 1.1,
                       'fleet_to_pehot': 0.6,
                       'fleet_to_fleet': 1.1,
                       'fleet_to_higth_fleet': 1.6,
                       'type_1_to_type_2': 100000000}
        a = (coord[0] - self.left) // self.cell_size
        b = (coord[1] - self.top) // self.cell_size
        if stat:
            a = coord[0]
            b = coord[1]
        if a == self.width - 1 or b == self.height -1 or (b not in range(self.height) or a not in range(self.width)):
            cota = 0
            if coord[0] in range(10, 560) and coord[1] in range(900, 1060):
                cota = 1
            elif coord[0] in range(570, 1120) and coord[1] in range(900, 1060):
                cota = 2
            if self.menu == 'City':
                if cota == 1:
                    self.bildings[self.ab].lvl_up(self.players['Human'])
                elif cota == 2:
                    tip = menu_of_selecting_type_of_unit(
                        self.board,
                        self.bildings[self.ab].position,
                        self.players['Human'],
                        self.screen,
                        self.bildings[self.ab]
                    )
                    self.bildings[self.ab].new_unit(self, tip, self.players['Human'])
            elif self.menu == 'IN':
                if cota == 1:
                    self.bildings[self.ab].lvl_up(self.players['Inseec'])
                elif cota == 2:
                    tip = menu_of_selecting_type_of_unit(
                        self.board,
                        self.bildings[self.ab].position,
                        self.players['Inseec'],
                        self.screen,
                        self.bildings[self.ab]
                    )
                    self.bildings[self.ab].new_unit(self, tip, self.players['Inseec'])
            elif self.menu == 'pehot' or self.menu == 'fleet' or self.menu == 'higth_fleet':
                if cota == 1 and self.active[0].hp != self.active[0].max_hp:
                    self.active[0].heal()
                    self.active[0].diactivate()
                    self.units[self.active[-1]] = self.active[0]
                    self.active = None
                if cota == 2:
                    self.new_bilding()
        elif self.board[b][a] in (2, 4, 5):
            stat = True
            if self.active:
                if self.position_of_unit([b, a]) == self.active[-1]:
                    self.active[0].diactivate()
                    self.units[self.active[-1]] = self.active[0]
                    stat = False
                    self.active = None
                elif (a, b) in self.active[0].alerts_show:
                    # бой
                    power_1 = self.units[self.active[1]].power
                    power_2 = self.units[self.position_of_unit([b, a])].power
                    type_1 = self.units[self.active[1]].type
                    type_2 = self.units[self.position_of_unit([b, a])].type
                    power_1 *= attack_unit[type_1 + '_to_' + type_2]  # Преимущество атаки)))
                    self.units[self.active[1]].hp -= power_2
                    self.units[self.position_of_unit([b, a])].hp -= power_1
                    self.active[0].had_been_activated_at_this_hod = True
                    if self.units[self.position_of_unit([b, a])].hp <= 0:
                        self.board[b][a] = self.board_clever[b][a]
                        if self.units[self.position_of_unit([b, a])].fraction == 'Human':
                            self.dead_human += 1
                        else:
                            self.dead_inseec += 1
                        del self.units[self.position_of_unit([b, a])]
                        self.active[0].sharik((b, a), stat=True)
                        self.active[0].diactivate()
                        self.units[self.active[-1]] = self.active[0]
                        self.active = None
                    elif self.units[self.active[1]].hp <= 0:
                        self.active[0].diactivate()
                        self.units[self.active[-1]] = self.active[0]
                        a, b = self.active[0].red_alert
                        self.board[b][a] = self.board_clever[b][a]
                        if self.units[self.active[1]].fraction == 'Human':
                            self.dead_human += 1
                        else:
                            self.dead_inseec += 1
                        del self.units[self.active[1]]
                        self.active = None
                    else:
                        self.active[0].diactivate()
                        self.units[self.active[-1]] = self.active[0]
                        self.active = None
                    if self.ab:
                        self.bildings[self.ab].diactivate()
                        self.ab = None
            elif self.units[self.position_of_unit([b, a])].had_been_activated_at_this_hod:
                # не даёт активироваться ранее активированному юниту
                pass
            elif self.hod == self.units[self.position_of_unit([b, a])].fraction and stat:
                # деактивация ранее активированного юнита
                if self.active and self.units[self.position_of_unit([b, a])].fraction == self.active[0].fraction:
                    self.active[0].diactivate()
                    self.units[self.active[-1]] = self.active[0]
                # Активация юнита
                if not self.units[self.position_of_unit([b, a])].healing:
                    self.active = (self.units[self.position_of_unit([b, a])].copy(), self.position_of_unit([b, a]))
                    self.active[0].activate()
                    self.active[0].render(self.screen)
                    self.units[self.active[-1]] = self.active[0]
        elif self.board[b][a] in (6, 7, 8):
            check_coord = [(b, a - 1), (b - 1, a), (b + 1, a), (b, a + 1), (b - 1, a - 1), (b - 1, a + 1),
                           (b + 1, a + 1), (b + 1, a - 1)]
            for x, y in check_coord:
                try:
                    if x < 0 or y < 0:
                        raise Exception
                except Exception as e:
                    pass
            if self.active and self.hod == self.bildings[self.position_of_bilding((b, a))].fraction:
                self.active[0].diactivate()
                self.active = None
            elif (self.active and self.hod != self.bildings[self.position_of_bilding((b, a))].fraction
                  and tuple(reversed(self.active[0].red_alert)) in check_coord):
                print(12345678)
                self.bildings[self.position_of_bilding((b, a))].hp -= self.active[0].power
                if self.bildings[self.position_of_bilding((b, a))].hp <= 0:
                    if self.bildings[self.position_of_bilding((b, a))].type == 'City':
                        self.board[b][a] = 0
                        self.alerts_city -= 1
                        self.destroid_city += 1
                    else:
                        if self.bildings[self.position_of_bilding((b, a))].type == 'IN':
                            self.alerts_inseec_nest -= 1
                            self.destroid_nests += 1
                        self.board[b][a] = 3
                    self.bildings_alerts -= 1
                    del self.bildings[self.position_of_bilding((b, a))]
                self.active[0].had_been_activated_at_this_hod = True
                self.active[0].diactivate()
                self.units[self.active[1]] = self.active[0]
                self.active = None
            if self.ab:
                self.bildings[self.ab].diactivate()
            # Активация постройки
            if self.position_of_bilding((b, a)) and self.board[b][a] != 7:
                if self.hod == self.bildings[self.position_of_bilding((b, a))].fraction:
                    self.bildings[self.position_of_bilding((b, a))].activate()
                    self.ab = self.position_of_bilding((b, a))
        elif self.active:
            # Перемещение активированного юнита
            if (a, b) in self.active[0].alerts_show:
                self.active[0].sharik((b, a), stat=True)
                self.active[0].had_been_activated_at_this_hod = True
                self.active[0].diactivate()
                self.units[self.active[-1]] = self.active[0]
                self.active = None

    def iteration(self):
        screen = self.screen
        self.update_units_data()
        if self.ab:
            self.bildings[self.ab].diactivate()
            self.ab = None
        # Совершение действий юнитов и построек
        for elem in self.units:
            elem = self.units[elem]
            elem.had_been_activated_at_this_hod = False
            elem.show = False
            if elem.activated:
                elem.diactivate()
                self.active = None
            if elem.moving:
                if elem.type == 'pehot':
                    x, y = elem.red_alert
                    if self.board_clever[y][x] == 2:
                        new = 0
                    else:
                        new = self.board_clever[y][x]
                    self.board[y][x] = new
                    elem.iteration()
                    x, y = elem.red_alert
                    self.board[y][x] = 2
                    elem.render(screen)
                if elem.type == 'fleet':
                    x, y = elem.red_alert
                    self.board[y][x] = 1
                    elem.iteration()
                    elem.iteration()
                    x, y = elem.red_alert
                    self.board[y][x] = 4
                    elem.render(screen)
                if elem.type == 'higth_fleet':
                    x, y = elem.red_alert
                    if self.board_clever[y][x] == 5:
                        new = 0
                    else:
                        new = self.board_clever[y][x]
                    self.board[y][x] = new
                    elem.iteration()
                    elem.iteration()
                    elem.iteration()
                    x, y = elem.red_alert
                    self.board[y][x] = 5
                    elem.render(screen)
        for elem in self.bildings:
            if self.bildings[elem].fraction == self.hod:
                self.bildings[elem].iteration(self, self.players[self.hod])
        # строительство построек
        for elem in self.bilder:
            self.board[elem[2]][elem[1]] = elem[0]
            if elem[0] == 6:
                self.alerts_city += 1
            elif elem[0] == 8:
                self.alerts_inseec_nest += 1
            self.bildings_alerts += 1
        self.bilder = []
        # проверка на конец игры
        if self.alerts_inseec_nest == 0 and self.inseec_alerts == 0:
            self.end_of_game('Human', self.screen)
        elif self.alerts_city == 0 and self.human_alerts == 0:
            self.end_of_game('Inseec', self.screen)
        # смена хода
        if self.hod == 'Human':
            self.hod = 'Inseec'
        else:
            self.hod = 'Human'

    def position_of_unit(self, coord):
        # ищет юнита в словаре self.units возвращает ключ к словарю
        coord = [coord[1], coord[0]]
        for elem in self.units:
            if self.units[elem].red_alert == coord:
                return elem

    def position_of_bilding(self, coord):
        # ищет постройку в словаре self.bildings возвращает ключ к словарю
        coord = [coord[1], coord[0]]
        for elem in self.bildings:
            if list(self.bildings[elem].position) == coord:
                return elem

    def update_units_data(self):
        # Смешные приколюшки для определения позиций юнитов для других юнитов
        self.inseec_alerts = 0
        self.human_alerts = 0
        for elem in self.units:
            elem = self.units[elem]
            main_elem = elem.red_alert
            if elem.fraction == 'Human':
                self.human_alerts += 1
            else:
                self.inseec_alerts += 1
            for obj in self.units:
                obj = self.units[obj]
                dop_elem = obj.red_alert
                if dop_elem != main_elem and elem.type == obj.type:
                    x, y = dop_elem
                    elem.board[x][y] = [0, -1]

    def new_bilding(self):
        # Какое здание ставить
        tob = menu_of_selecting_type_of_bilding(self.board_clever, self.active[0], self.players[self.hod], self.screen)
        if not tob:
            return None
        if self.board[tob[1][0]][tob[1][1]] != 0:
            return None
        b, a = self.active[0].red_alert.copy()
        self.active[0].had_been_activated_at_this_hod = True
        self.click(list(reversed(tob[1])), stat=True)
        if tob[0] == 'City':
            self.players[self.hod].resuorce -= 500
            self.bilder.append((6, b, a))
        elif tob[0] == 'RS':
            self.players[self.hod].resuorce -= 150
            self.bilder.append((7, b, a))
        elif tob[0] == 'IN':
            self.players[self.hod].resuorce -= 500
            self.bilder.append((8, b, a))

    def make_save(self):
        karta = open(r'data\lvls\save1\map.txt', 'w')
        for elem in self.board:
            for obj in elem:
                karta.write(str(obj))
            karta.write('\n')
        data_save = open(r'data\lvls\save1\lvl_data.txt', 'w')
        spisok = []
        for elem in self.units:
            spisok.append(self.units[elem].atributs())
        data_save.write(str(spisok))
        data_save.write('\n')
        spisok = []
        for elem in self.bildings:
            spisok.append(self.bildings[elem].atributs())
        data_save.write(str(spisok))
        data_save.write('\n')
        data_save.write(str(self.hod))
        data_save.write('\n')
        stroka = str(self.destroid_nests) + ' ' + str(self.destroid_city) + ' ' + str(self.dead_human) + ' '
        stroka += str(self.dead_inseec) + str(self.alerts_city) + ' ' + str(self.alerts_inseec_nest)
        data_save.write(stroka)
        data_save.write('\n')
        stroka = str(self.players['Human'].resuorce) + ' ' + str(self.players['Inseec'].resuorce)
        data_save.write(stroka)

    def read_save(self, save_pos):
        self.active = None
        self.ab = None
        self.units = dict()
        self.bildings = dict()
        data_save = open(rf'data\lvls\save{str(save_pos)}\lvl_data.txt', 'r').readlines()
        self.board = readmap(rf'data\lvls\save{str(save_pos)}\map.txt')
        self.board_clever = readmap(rf'data\lvls\save{str(save_pos)}\map.txt', True)
        self.alerts = sum([elem.count(2) + elem.count(4) + elem.count(5) for elem in self.board])
        self.bildings_alerts = sum([elem.count(6) + elem.count(7) + elem.count(8) for elem in self.board])
        count = 0
        self.water_unit_wall = Unit(self.width, self.height)
        self.water_unit_wall.set_view(self.left, self.top, self.cell_size)
        self.rock_unit_wall = Unit(self.width, self.height)
        self.water_unit_wall.set_view(self.left, self.top, self.cell_size)
        self.earth_unit_wall = Unit(self.width, self.height)
        self.water_unit_wall.set_view(self.left, self.top, self.cell_size)
        for elem in eval(data_save[0][:-1]):
            unit = self.water_unit_wall.copy()
            unit.type = elem['type']
            if 'red_alert' in elem:
                unit.red_alert = elem['red_alert']
            if 'alerts' in elem:
                unit.alerts = elem['alerts']
            unit.board = elem['board']
            unit.fraction = elem['fraction']
            unit.hp = elem['hp']
            unit.healing = elem['healing']
            unit.power = elem['power']
            unit.max_hp = elem['max_hp']
            self.units['Unit' + str(count)] = unit
            count += 1
        count = 0
        cell_size = 40
        for elem in eval(data_save[1][:-1]):
            if elem['type'] == 'City':
                i, j = elem['position']
                city = City((i, j), self.left, self.top, self.cell_size, self.screen)
                city.set_view(self.left, self.top, cell_size)
                city.hp = elem['hp']
                city.cop = elem['cop']
                city.lvl = elem['lvl']
                city.max_hp = elem['max_hp']
                self.bildings['City' + str(count)] = city
                count += 1
            elif elem['type'] == 'RS':
                i, j = elem['position']
                rs = RS((i, j), self.left, self.top, self.cell_size, self.screen)
                rs.set_view(self.left, self.top, cell_size)
                rs.hp = elem['hp']
                self.bildings['RS' + str(count)] = rs
                count += 1
            elif elem['type'] == 'IN':
                i, j = elem['position']
                nest = IN((i, j), self.left, self.top, self.cell_size, self.screen)
                nest.set_view(self.left, self.top, cell_size)
                nest.hp = elem['hp']
                nest.cop = elem['cop']
                nest.lvl = elem['lvl']
                nest.max_hp = elem['max_hp']
                self.bildings['RS' + str(count)] = nest
                count += 1
        alerts = data_save[3][:-1:].split()
        self.alerts_inseec_nest = int(alerts[-1])
        self.alerts_city = int(alerts[-2])
        self.dead_inseec = int(alerts[-3])
        self.dead_human = int(alerts[-4])
        self.destroid_city = int(alerts[-5])
        self.destroid_nests = int(alerts[0])
        self.players['Human'].resuorce = int(data_save[4].split()[0])
        self.players['Inseec'].resuorce = int(data_save[4].split()[1])
        self.hod = data_save[2][:-1:]

    def end_of_game(self, winner, screen):
        print('lol')
        image = pygame.image.load(rf'data\sprites\end.png')
        screen.blit(image, (0, 0))
        font = pygame.font.Font(None, 120)
        if winner == 'Human':
            text_surface = font.render('Люди', True, 'White')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (640, 98)
            screen.blit(text_surface, text_rect)
        else:
            text_surface = font.render('Инсееки', True, 'White')
            text_rect = text_surface.get_rect()
            text_rect.midtop = (640, 98)
            screen.blit(text_surface, text_rect)
        text_surface = font.render(str(self.destroid_nests), True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (1100, 274)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(self.destroid_city), True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (1220, 454)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(self.dead_inseec), True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (900, 654)
        screen.blit(text_surface, text_rect)
        text_surface = font.render(str(self.dead_human), True, 'White')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (800, 850)
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, 'Yellow', ((0, 0), (1920, 1080)), 5)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        vihod()
