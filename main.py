from FC import *
from board import Board


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("РЕСУРС")

    def new_game(self):
        lvl = menu_of_choosing_lvl(self.screen)
        if lvl:
            pygame.init()
            it = True
            while it:
                try:
                    filename = fr'lvls\main_loc\{lvl}'
                    card = readmap(fr'''data\{filename}.txt''')
                    it = False
                except Exception as a:
                    print('error of file name')
            whidth = len(card[0]) - 2
            height = len(card)
            cell_size = 40
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            board = Board(whidth + 2, height - 3, fr'data/{filename}.txt', screen)
            board.set_view(-cell_size, -cell_size, cell_size)
            running = True
            clock = pygame.time.Clock()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        board.click(event.pos)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            board.iteration()
                        if event.key == pygame.K_ESCAPE:
                            running = menu_of_pause(screen, board)
                        if event.key == pygame.K_F6:
                            board.read_save(1)
                        if event.key == pygame.K_F5:
                            board.make_save()
                board.render()
                clock.tick(60)
                pygame.display.flip()
        self.draw_menu()

    def donate(self):
        donate_animation(self.screen)
        self.draw_menu()

    def exit_game(self):
        return False

    def load_save(self):
        lvl = 'map'
        if lvl:
            pygame.init()
            it = True
            while it:
                try:
                    filename = fr'lvls\main_loc\{lvl}'
                    card = readmap(fr'''data\{filename}.txt''')
                    it = False
                except Exception as a:
                    print('error of file name')
            whidth = len(card[0]) - 2
            height = len(card)
            cell_size = 40
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            board = Board(whidth + 2, height - 3, fr'data/{filename}.txt', screen)
            board.set_view(-cell_size, -cell_size, cell_size)
            running = True
            try:
                board.read_save(1)
            except Exception as e:
                running = False
            clock = pygame.time.Clock()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        board.click(event.pos)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            board.iteration()
                        if event.key == pygame.K_ESCAPE:
                            running = menu_of_pause(screen, board)
                        if event.key == pygame.K_F6:
                            board.read_save(1)
                        if event.key == pygame.K_F5:
                            board.make_save()
                board.render()
                clock.tick(60)
                pygame.display.flip()
        self.draw_menu()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (50, 50, 50), (1920//2-840//2, 130, 840, 830))  # красная хрень посередине
        pygame.draw.rect(self.screen, (178, 34, 34), (1920//2-760//2, 150, 760, 170))
        pygame.draw.rect(self.screen, (178, 34, 34), (1920//2-760//2, 350, 760, 170))
        pygame.draw.rect(self.screen, (178, 34, 34), (1920//2-760//2, 550, 760, 170))
        pygame.draw.rect(self.screen, (178, 34, 34), (1920//2-760//2, 750, 760, 170))
        button_font = pygame.font.Font(None, 100)
        button1 = button_font.render('Загрузка сохранения', True, 'white')
        button2 = button_font.render('Новая игра', True, 'white')
        button3 = button_font.render('Выйти из игры', True, 'white')
        button4 = button_font.render('Задонатить', True, 'white')
        self.screen.blit(button1, (600, 600))  # тексты
        self.screen.blit(button2, (770, 200))
        self.screen.blit(button3, (720, 800))
        self.screen.blit(button4, (770, 400))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if 1920//2-760//2 <= mouse_pos[0] <= 1920//2+760//2:
                            if 150 <= mouse_pos[1] <= 320:
                                self.new_game()
                            elif 350 <= mouse_pos[1] <= 520:
                                self.donate()
                            elif 550 <= mouse_pos[1] <= 720:
                                self.load_save()
                            elif 750 <= mouse_pos[1] <= 920:
                                running = self.exit_game()


Menu().draw_menu()
