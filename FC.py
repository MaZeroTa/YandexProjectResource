# Functions, Consts
import pygame
import time


def readmap(filename, stat=False):
    card = open(filename, 'r').readlines()
    itog = []
    for elem in card:
        proto = []
        for obj in elem[::]:
            try:
                if stat:
                    if int(obj) in (0, 1, 3):
                        proto.append(int(obj))
                    elif int(obj) == 4:
                        proto.append(1)
                    elif int(obj) in (7, 8):
                        proto.append(3)
                    else:
                        proto.append(0)
                else:
                    proto.append(int(obj))
            except Exception as e:
                pass
        itog.append(proto)
    return itog


def menu_of_selecting_type_of_unit(board, position, player, screen, bilding):
    pygame.draw.rect(screen, (50, 50, 50), (760, 220, 400, 580))
    pygame.draw.rect(screen, (0, 0, 0), (760, 220, 400, 580), 4)
    pygame.draw.rect(screen, (20, 20, 20), (780, 250, 360, 160))
    pygame.draw.rect(screen, (20, 20, 20), (780, 430, 360, 160))
    pygame.draw.rect(screen, (20, 20, 20), (780, 610, 360, 160))
    font = pygame.font.Font(None, 70)
    text_surface = font.render(f'Пехота - {100 * bilding.cop}', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 310)
    screen.blit(text_surface, text_rect)
    text_surface = font.render(f'Флот - {200 * bilding.cop}', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 490)
    screen.blit(text_surface, text_rect)
    text_surface = font.render(f'Авиация - {300 * bilding.cop}', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 670)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    menu_status = True
    while menu_status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click(event.pos, 'unit') == 'pehot':
                    if player.resuorce < 100:
                        pass
                    else:
                        return 'pehot'
                elif click(event.pos, 'unit') == 'fleet':
                    if player.resuorce < 150:
                        pass
                    else:
                        return 'fleet'
                elif click(event.pos, 'unit') == 'higth_fleet':
                    if player.resuorce < 250:
                        pass
                    else:
                        return 'higth_fleet'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_status = False


def menu_of_selecting_type_of_bilding(board, unit, player, screen):
    font = pygame.font.Font(None, 70)
    if unit.fraction == 'Human':
        pygame.draw.rect(screen, (50, 50, 50), (760, 220, 400, 580))
        pygame.draw.rect(screen, (0, 0, 0), (760, 220, 400, 580), 4)
        pygame.draw.rect(screen, (20, 20, 20), (780, 240, 360, 260))
        pygame.draw.rect(screen, (20, 20, 20), (780, 520, 360, 260))
        text_surface = font.render('Город - 500', True, 'WHITE')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (960, 340)
        screen.blit(text_surface, text_rect)
        text_surface = font.render('Шахта - 150', True, 'WHITE')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (960, 620)
        screen.blit(text_surface, text_rect)
    elif unit.fraction == 'Inseec':
        pygame.draw.rect(screen, (50, 50, 50), (760, 220, 400, 300))
        pygame.draw.rect(screen, (0, 0, 0), (760, 220, 400, 300), 4)
        pygame.draw.rect(screen, (20, 20, 20), (780, 240, 360, 260))
        text_surface = font.render('Город - 500', True, 'WHITE')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (960, 340)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
    menu_status = True
    while menu_status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click(event.pos, 'bild') == 'City':
                    coord = unit.red_alert
                    if not look_around(board, coord):
                        pass
                    elif player.resuorce < 500:
                        pass
                    else:
                        if unit.fraction == 'Human' and board[coord[1]][coord[0]] == 0:
                            return ('City', look_around(board, coord))
                        elif board[coord[1]][coord[0]] == 0 and unit.fraction == 'Inseec':
                            return ('IN', look_around(board, coord))
                elif click(event.pos, 'bild') == 'RS':
                    coord = unit.red_alert
                    if board[coord[1]][coord[0]] != 3:
                        pass
                    elif not look_around(board, coord):
                        pass
                    elif player.resuorce < 150:
                        pass
                    else:
                        return ('RS', look_around(board, coord))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_status = False


def menu_of_pause(screen, board):
    pygame.draw.rect(screen, (50, 50, 50), (690, 200, 540, 550))
    pygame.draw.rect(screen, (0, 0, 0), (690, 200, 540, 550), 4)
    pygame.draw.rect(screen, (178, 34, 34), (730, 240, 460, 70))
    pygame.draw.rect(screen, (178, 34, 34), (730, 340, 460, 70))
    pygame.draw.rect(screen, (178, 34, 34), (730, 440, 460, 70))
    pygame.draw.rect(screen, (178, 34, 34), (730, 540, 460, 70))
    pygame.draw.rect(screen, (178, 34, 34), (730, 640, 460, 70))
    font = pygame.font.Font(None, 45)
    text_surface = font.render('ВЫХОД В ГЛАВНОЕ МЕНЮ', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 260)
    screen.blit(text_surface, text_rect)
    text_surface = font.render('ВЫЙТИ ИЗ ИГРЫ', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 360)
    screen.blit(text_surface, text_rect)
    text_surface = font.render('ЗАГРУЗИТЬ СОХРАНЕНИЕ', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 460)
    screen.blit(text_surface, text_rect)
    text_surface = font.render('СОХРАНИТЬ ПРОГРЕСС', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 560)
    screen.blit(text_surface, text_rect)
    text_surface = font.render('ВЕРНУТЬСЯ', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 660)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    menu_status = True
    while menu_status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                vid = 'pause'
                if click(pos, vid, board) == 1:
                    menu_status = False
                if not click(pos, vid, board):
                    return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_status = False
    return True


def menu_of_choosing_lvl(screen, board=None):
    pygame.draw.rect(screen, (50, 50, 50), (690, 200, 540, 330))
    pygame.draw.rect(screen, (0, 0, 0), (690, 200, 540, 330), 4)
    pygame.draw.rect(screen, (178, 34, 34), (730, 240, 460, 70))
    pygame.draw.rect(screen, (178, 34, 34), (730, 340, 460, 70))
    pygame.draw.rect(screen, (178, 34, 34), (730, 440, 460, 70))
    font = pygame.font.Font(None, 45)
    text_surface = font.render('Остров', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 260)
    screen.blit(text_surface, text_rect)
    text_surface = font.render('Архипелаг', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 360)
    screen.blit(text_surface, text_rect)
    text_surface = font.render('Материк', True, 'WHITE')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (960, 460)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    menu_status = True
    while menu_status:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                vid = 'lvl'
                return click(pos, vid, board)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_status = False


def click(pos, vid, board=None):
    if pos[0] in range(780, 1140) and pos[1] in range(240, 500) and vid == 'bild':
        return 'City'
    elif pos[0] in range(780, 1140) and pos[1] in range(520, 780) and vid == 'bild':
        return 'RS'
    if pos[0] in range(780, 1140) and pos[1] in range(250, 410) and vid == 'unit':
        return 'pehot'
    elif pos[0] in range(780, 1140) and pos[1] in range(430, 590) and vid == 'unit':
        return 'fleet'
    elif pos[0] in range(780, 1140) and pos[1] in range(610, 770) and vid == 'unit':
        return 'higth_fleet'
    elif vid == 'pause' and pos[0] in range(730, 1191):
        if pos[1] in range(240, 311):
            return False
        elif pos[1] in range(340, 411):
            exit()
        elif pos[1] in range(440, 511):
            board.read_save(1)
        elif pos[1] in range(540, 611):
            board.make_save()
        elif pos[1] in range(640, 711):
            return 1
        return True
    elif vid == 'lvl' and pos[0] in range(730, 1191):
        if pos[1] in range(240, 311):
            return 'first_island'
        elif pos[1] in range(340, 411):
            return 'archipelag'
        elif pos[1] in range(440, 511):
            return 'Continent'
        return True


def look_around(board, coord):
    x, y = coord[1], coord[0]
    alert = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    for x, y in alert:
        try:
            if x < 1 or y < 1:
                raise Exception
            if board[x][y] == 0:
                return x, y
        except Exception as e:
            pass


def donate_animation(screen):
    class Car(pygame.sprite.Sprite):
        def __init__(self, filename):
            W = 1920
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = W

        def update(self, screen):
            W = 1920
            if W - self.rect.x != W:
                self.rect.x -= 5

    car = Car(r'data/sprites/Donat.png')
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((0, 0, 0))
        screen.blit(car.image, car.rect)
        car.update(screen)
        pygame.display.flip()
        clock.tick(200)
