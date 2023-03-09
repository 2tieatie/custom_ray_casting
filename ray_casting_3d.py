import pygame, sys, os
import time
import math


map = ['000000',
       '00---0',
       '0-0-00',
       '0---00',
       '0-0--0',
       '0--0-0',
       '000000']


world_map = set()



for i, row in enumerate(map):
    for i1, char in enumerate(row):
        if char == '0':
            world_map.add((i1*100, i*100))


class Player():
    def __init__(self, screen, world_map):
        self.wm = world_map
        self.screen = screen
        self.pos = pygame.mouse.get_pos()
        self.mouse_x = self.pos[0]
        self.mouse_y = self.pos[1]
        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(0 - 5, 0 - 5, 10, 10)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.move_right = False
        self.move_left = False
        self.move_down = False
        self.move_up = False
        self.pl_a_v = round(math.pi / 6, 2)
        self.dist = 150 / (2 * math.tan(self.pl_a_v))
        self.coeff = 2 * self.dist * 60
        self.scale = 600 / 150


    def draw_player(self):
        self.pos = pygame.mouse.get_pos()
        self.mouse_x = self.pos[0]
        self.mouse_y = self.pos[1]
        self.angle = math.atan2(self.screen_rect.centery - self.mouse_y, self.screen_rect.centerx - self.mouse_x)
        self.start_pos = self.rect.center
        self.end_point = [self.rect.centerx, self.rect.centery]
        for ray in range(-75, 75):
            sin_a = math.sin(self.angle - ray/450)
            cos_a = math.cos(self.angle - ray/450)
            for depth in range(600):
                self.end_point[0] = self.start_pos[0] - depth * cos_a
                self.end_point[1] = self.start_pos[1] - depth * sin_a
                # pygame.draw.line(self.screen, (0, 255, 0), self.start_pos, self.end_point, 2)
                depth +=1
                if (self.end_point[0] // 100 * 100, self.end_point[1] // 100 * 100) in self.wm:
                    self.rects_height = self.coeff / depth
                    c = 255 / (1 + depth ** 2 * 0.0001)
                    self.color = (c, 0, 0)
                    depth *= cos_a
                    pygame.draw.rect(self.screen, self.color, (300 + ray * self.scale, 300 - self.rects_height // 2, self.scale, self.rects_height))
                    break
        pygame.draw.circle(self.screen, (0, 0, 255), self.screen_rect.center, 3)
        # pygame.draw.circle(self.screen, (0, 0, 255), (self.rect.centerx, self.rect.centery), 5)

    def cursor_select(self):
        self.mouse_x = self.pos[0]
        self.mouse_y = self.pos[1]
        pygame.draw.circle(self.screen, (75, 20, 20), (self.mouse_x, self.mouse_y), 8)

    def move(self):
        self.angle_1 = math.atan2(self.screen_rect.centery - self.mouse_y, self.screen_rect.centerx - self.mouse_x)
        if self.move_up:
            self.rect.centerx -= math.cos(self.angle_1) * 2.75
            self.rect.centery -= math.sin(self.angle_1) * 2.75
        elif self.move_down:
            self.rect.centerx += math.cos(self.angle_1) * 2.75
            self.rect.centery += math.sin(self.angle_1) * 2.75
        elif self.move_left:
            self.rect.centerx += math.cos(self.angle_1 - math.pi/4) * 2.75
        elif self.move_right:
            self.rect.centerx -= math.cos(self.angle_1 + math.pi/4) * 2.75



    def draw_map(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.rect.centerx / 10, self.rect.centery / 10), 2)
        pygame.draw.line(self.screen, (0, 255, 0), (self.rect.centerx / 10, self.rect.centery / 10), (
        self.rect.centerx / 10 - math.cos(self.angle_1) * 15, self.rect.centery / 10 - math.sin(self.angle_1) * 15), 1)
        for x, y in self.wm:
            pygame.draw.rect(self.screen, (0, 0, 0), (x/10, y/10, 10, 10))
def fps(screen, clock):
    font = pygame.font.SysFont(None, 40)
    fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0), None)
    fps_rect = fps.get_rect()
    fps_rect.centerx = 530
    fps_rect.centery = 30
    screen.blit(fps, fps_rect)

def events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move_up = True
            elif event.key == pygame.K_s:
                player.move_down = True
            elif event.key == pygame.K_a:
                player.move_left = True
            elif event.key == pygame.K_d:
                player.move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.move_up = False
            elif event.key == pygame.K_s:
                player.move_down = False
            elif event.key == pygame.K_a:
                player.move_left = False
            elif event.key == pygame.K_d:
                player.move_right = False


def run(Player):
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    player = Player(screen, world_map)
    clock = pygame.time.Clock()
    while True:
        clock.tick(65)
        events(player)
        player.move()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 237, 0), (0, 300, 1200, 600))
        pygame.draw.rect(screen, (0, 0, 255), (0, 0, 1200, 300))

        player.draw_player()
        player.cursor_select()
        player.draw_map()
        fps(screen, clock)
        pygame.display.flip()


run(Player)












