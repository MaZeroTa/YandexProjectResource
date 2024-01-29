import pygame


class RS:
    def __init__(self, coord, left, top, cell_size, screen):
        self.fraction = 'Human'
        self.position = coord
        self.type = 'RS'
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.screen = screen
        self.power = 100
        self.activated = False
        self.hp = 100

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
        center = (lt[0] + self.cell_size / 2, lt[1] + self.cell_size / 2)
        im = pygame.image.load(r'data\sprites\mining.png').convert_alpha()
        self.screen.blit(im, (lt, rt))
        if 100 != self.hp:
            lt = (lt[0] + 10, lt[1] + 30)
            rd = (20, 5)
            pygame.draw.rect(self.screen, (20, 20, 20), (lt, rd))
            lt = (lt[0] + 1, lt[1] + 1)
            rd = (int(18 * (self.hp / 100)), 4)
            pygame.draw.rect(self.screen, 'GREEN', (lt, rd))

    def iteration(self, board, player):
        player.resuorce += 50
        if self.hp < 100:
            self.hp += 15
            if self.hp > 100:
                self.hp = 100

    def atributs(self):
        # Система для сейва
        atributs = {
            'type': 'RS',
            'cell_size': self.cell_size,
            'position': self.position,
            'hp': self.hp
        }
        return atributs


