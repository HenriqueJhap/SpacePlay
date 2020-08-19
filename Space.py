
# * Imports
import pygame, random
from pygame.locals import *

#* Boots
pygame.init()
clock = pygame.time.Clock()

# * Constants
FONT = pygame.font.SysFont("comicsans", 50)
LOST_FONT = pygame.font.SysFont("comicsans", 60)

SCREEN_HEIGHT = 650
SCREEN_WIDTH = 800

BACK_POS_WIDTH = 0
BACK_SPEED = 7

SHIPPLAYER_POS_HEIGHT = 550
SHIPPLAYER_POS_WIDTH = SCREEN_WIDTH / 2 - 20
SHIPPLAYER_HEIGHT = 60
SHIPPLAYER_WIDTH = 60
PLAYER_SPEED = 10

LASERSPEED = 3

# * Variables
Level = 1
Lives = 5
Wave_Length = 5
Enemy_Speed = 2
LostCount = 0

# * Images
IMAGE_BACK = pygame.image.load('background-black.png')
IMAGE_BACK = pygame.transform.scale(IMAGE_BACK,(SCREEN_WIDTH,SCREEN_HEIGHT))

IMAGE_SHIPPLAYER = pygame.image.load('pixel_ship_yellow.png')
IMAGE_SHIPPLAYER = pygame.transform.scale(IMAGE_SHIPPLAYER,(SHIPPLAYER_WIDTH,SHIPPLAYER_HEIGHT))
IMAGE_SHIPRED = pygame.image.load('pixel_ship_red_small.png')
IMAGE_SHIPBLUE = pygame.image.load('pixel_ship_blue_small.png')
IMAGE_SHIPGREEN = pygame.image.load('pixel_ship_green_small.png')

IMAGE_LASERPLAYER = pygame.image.load('pixel_laser_yellow.png')
IMAGE_LASERRED = pygame.image.load('pixel_laser_red.png')
IMAGE_LASERBLUE = pygame.image.load('pixel_laser_blue.png')
IMAGE_LASERGREEN = pygame.image.load('pixel_laser_green.png')

# *Classes
class Background(pygame.sprite.Sprite):
    def __init__(self, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = IMAGE_BACK

        self.rect = self.image.get_rect()
        self.rect[0] = BACK_POS_WIDTH # *Width initial
        self.rect[1] = ypos # *Height  initial
    
    #* movement back
    def update(self):
        self.rect[1] += BACK_SPEED

class Laser(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ypos

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.image == IMAGE_LASERPLAYER: #*moviment laser player
            self.rect[1] -= LASERSPEED
        else: # *moviment laser enemy
            self.rect[1] += LASERSPEED

class Ship(pygame.sprite.Sprite):
    
    def __init__(self, xpos, ypos, max_cooldown = 100):
        pygame.sprite.Sprite.__init__(self)

        self.ship_img = IMAGE_SHIPPLAYER
        self.laser_img = IMAGE_LASERPLAYER
        self.Lasers = []
        
        self.rect = self.ship_img.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ypos

        self.cool_down_counter = 0 # * counter time of shoots
        self.max_cooldown = max_cooldown # * time of shoots
    
    def cooldown(self): #* Function time shoot
        if self.cool_down_counter >= self.max_cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self): # * Function shoot laser
        if self.cool_down_counter == 0:
            laser = Laser(self.rect[0] + self.ship_img.get_width() / 2 - self.laser_img.get_width() / 2 , self.rect[1], self.laser_img)
            Laser_Group.add(laser)
            self.Lasers.append(laser)
            self.cool_down_counter = 1
                  
class Player(Ship,pygame.sprite.Sprite):
    def __init__(self, xpos,ypos, max_cooldown):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(xpos,ypos, max_cooldown)
        
        self.image = IMAGE_SHIPPLAYER
        self.laser_img = IMAGE_LASERPLAYER
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100 # * Health player

    def update(self):
        pass

    def draw_health(self):
        # * life bar red
        pygame.draw.rect(screen, (255,0,0), (self.rect[0] , self.rect[1] + self.image.get_height() + 10, self.image.get_width(), 10))
        # * life bar green
        pygame.draw.rect(screen, (0,255,0), (self.rect[0] , self.rect[1] + self.image.get_height() + 10, self.image.get_width() * (self.health / 100), 10))
        
    #*functions moviment ship    
    def move_up(self):
        self.rect[1] -= PLAYER_SPEED
    def move_low(self):
        self.rect[1] += PLAYER_SPEED
    def move_left(self):
        self.rect[0] -= PLAYER_SPEED
    def move_right(self):
        self.rect[0] += PLAYER_SPEED  

class Enemy(Ship,pygame.sprite.Sprite):
    COLOR_MAP = {
        "red": (IMAGE_SHIPRED,IMAGE_LASERRED),
        "blue": (IMAGE_SHIPBLUE,IMAGE_LASERBLUE),
        "green": (IMAGE_SHIPGREEN,IMAGE_LASERGREEN)

    }

    def __init__(self, xpos, ypos, color):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(xpos,ypos)
        self.image, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        self.rect[1] += Enemy_Speed

# *Boot Groups
Back_Group = pygame.sprite.Group()
for i in range(2):
    Back = Background(-i * SCREEN_HEIGHT)
    Back_Group.add(Back)

Laser_Group = pygame.sprite.Group()

Player_Group = pygame.sprite.Group()
player = Player(SCREEN_WIDTH /2 - SHIPPLAYER_WIDTH / 2, SCREEN_HEIGHT - SHIPPLAYER_HEIGHT -30, 30)
Player_Group.add(player)

Enemy_Group = pygame.sprite.Group()
for i in range(Wave_Length):
            new_enemy = Enemy(random.randrange(50,SCREEN_WIDTH-100), random.randrange(-1500,-100),
                        random.choice(["red","blue","green"]))
            Enemy_Group.add(new_enemy)

# *Functions
def is_off_screen(sprite, UpAndDown):
    if(UpAndDown):
        return (sprite.rect[1] > SCREEN_HEIGHT or sprite.rect[1] < 0)
    else:
        return sprite.rect[1] > SCREEN_HEIGHT

# *Screen and Title
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("SPACE")

# *Loppin PLAY
while True:
    #*delay
    clock.tick(60)

    #!test END PLAY
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    if LostCount > 60 * 3:
        pygame.quit()
    
    # ! Mensage of lost
    if(Lives <= 0):
        lost_label = LOST_FONT.render("YOU LOST!!",1,(255,255,255))
        screen.blit(lost_label,(SCREEN_WIDTH /2 - lost_label.get_width() /2, 350))
        LostCount += 1
        
    #* Play
    else:
        #*Function time of shoot
        player.cooldown()

        #*test commands moviment ship player
        commands = pygame.key.get_pressed()
        if commands[pygame.K_UP] and (player.rect[1] - PLAYER_SPEED > 0):
            player.move_up()
        if commands[pygame.K_DOWN] and (player.rect[1] + PLAYER_SPEED + SHIPPLAYER_HEIGHT + 30 < SCREEN_HEIGHT):
            player.move_low()
        if commands[pygame.K_RIGHT] and (player.rect[0] + PLAYER_SPEED + SHIPPLAYER_WIDTH < SCREEN_WIDTH):
            player.move_right()
        if commands[pygame.K_LEFT] and (player.rect[0] - PLAYER_SPEED > 0):
            player.move_left()
        if commands[pygame.K_SPACE]:
            player.shoot()

        #*tests of-screen, remove sprites off-screen, create news sprites
        if is_off_screen(Back_Group.sprites()[0],False):
            Back_Group.remove(Back_Group.sprites()[0])
            New_Back = Background(-SCREEN_HEIGHT - 10)
            Back_Group.add(New_Back)

        for laser in Laser_Group:
            if (is_off_screen(laser, True)):
                Laser_Group.remove(laser)
            
        for enemy in Enemy_Group:
            if is_off_screen(enemy,False):
                Lives -= 1
                Enemy_Group.remove(enemy)

        #* Shoots Enemy
        for enemy in Enemy_Group:
            if is_off_screen(enemy, True) == False:
                enemy.cooldown()
                enemy.shoot()

        #*Collisions
        for laser in Laser_Group: # * Colission ship and laser
            if laser.image == IMAGE_LASERPLAYER: # * Colission laser player and enemy
                for enemy in Enemy_Group:
                    if pygame.sprite.collide_mask(enemy,laser):
                        for laser_enemy in enemy.Lasers:
                            Laser_Group.remove(laser_enemy)
                        Enemy_Group.remove(enemy)
            
            else: #* Colission enemy laser and player
                if pygame.sprite.collide_mask(player,laser):
                    Laser_Group.remove(laser)
                    player.health -= 10

        for enemy in Enemy_Group:#*Collision player and Enemy
            if pygame.sprite.collide_mask(enemy,player):
                for laser_enemy in enemy.Lasers:
                    Laser_Group.remove(laser_enemy)
                Enemy_Group.remove(enemy)
                player.health -= 10

        #* Test of life
        if player.health <= 0:
            player.health = 100
            Lives -= 1

        # * New Wave
        if len(Enemy_Group) == 0:
            Level += 1
            player.health = 100
            Lives += 1
            Wave_Length += 5
            for i in range(Wave_Length):
                new_enemy = Enemy(random.randrange(50,SCREEN_WIDTH-100), random.randrange(-1500,-100),
                        random.choice(["red","blue","green"]))
                Enemy_Group.add(new_enemy)

        #*updates sprites
        Back_Group.update()
        Player_Group.update()
        Enemy_Group.update()
        Laser_Group.update()

        #*draws sprites
        Back_Group.draw(screen)
        Player_Group.draw(screen)
        Enemy_Group.draw(screen)
        Laser_Group.draw(screen)
        player.draw_health()

        #*draws lives and level
        lives_label = FONT.render(f"Lives: {Lives}",1,(255,255,255))
        level_label = FONT.render(f"Level: {Level}",1,(255,255,255))
        screen.blit(lives_label,(10,10))
        screen.blit(level_label,(SCREEN_WIDTH - level_label.get_width(),0))
    
    pygame.display.update()