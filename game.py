
import pygame
from pygame.locals import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.Surface((30,10),pygame.SRCALPHA)
        self.surf.fill((0,0,0))
        self.surf.set_colorkey((0,0,0))
        self.points = [[0,0],[24,0],[30,5],[24,10],[0,10]]
        pygame.draw.polygon(self.surf,pygame.Color('dodgerblue'),self.points)
        self.org_surf = self.surf.copy()
        self.angle = math.pi / 2
        self.rect = self.surf.get_rect(center=(50,200))
        self.mask = pygame.mask.from_surface(self.surf)

    def update(self,pressed_keys):
        distance = 0
        if pressed_keys[K_UP]: distance +=4
        if pressed_keys[K_DOWN]: distance -=4
        if pressed_keys[K_LEFT]: self.angle += 0.03
        if pressed_keys[K_RIGHT]: self.angle -= 0.03

        self.surf = pygame.transform.rotate(self.org_surf, 270 + self.angle / 3.14 * 180)

        move_x= math.sin(self.angle)*distance
        move_y= math.cos(self.angle)*distance
        self.rect.move_ip(move_x,move_y)

class War(pygame.sprite.Sprite):
    def __init__(self,pointlist):
        super(War,self).__init__()
        self.surf = pygame.Surface((640,480),pygame.SRCALPHA)
        pygame.draw.lines(self.surf,(255,255,255),False,pointlist,12)
        self.rect = self.surf.get_rect(center=(320,240))
        self.mask = pygame.mask.from_surface(self.surf)

def DetectCollision(war1,war2,player):
    offset_x1 = player.rect.x - war1.rect.x
    offset_y1 = player.rect.y - war1.rect.y

    offset_x2 = player.rect.x - war2.rect.x
    offset_y2 = player.rect.y - war2.rect.y


    overlap1 = war1.mask.overlap(player.mask,(offset_x1,offset_y1))
    overlap2 = war2.mask.overlap(player.mask,(offset_x2,offset_y2))
    return overlap1 or overlap2


def main():
    pygame.init()

    pointlist1 = [[60,160],[300,80],[600,230]]
    pointlist2 = [[60,260],[300,180],[600,330]]

    war1 = War(pointlist1)
    war2 = War(pointlist2)
    player = Player()

    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    pygame.display.set_caption("xrr")
    font1 = pygame.font.SysFont('arial',30)
    text1 = font1.render("Game Over",True,(255,255,255))

    #pygame.mixer.music.load('music.mp3')
    #pygame.mixer_music.play(-1,0)

    running = True
    game = True

    while running:
        if not game:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game = True
                        player.rect.center=(50,200)
                elif event.type == QUIT:
                    running = False
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)

            screen.fill((0,0,0))
            if DetectCollision(war1,war2,player):
                game = False
                screen.blit(text1,(320,240))
            else:
                screen.blit(player.surf,player.rect)
                screen.blit(war1.surf,war1.rect)
                screen.blit(war2.surf,war2.rect)
            pygame.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    main()


