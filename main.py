import pygame
from random import randint
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT
)

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 500

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("Space Shooter/Assets/Player_ship.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.size = self.image.get_size()
        self.surf = pygame.transform.scale(self.image, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.surf.get_rect(
            center = (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 40
            )
        )
        self.health = 5
        self.score = 0
    
    def update(self, pressed_keys):
        #move sprite
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT     

    def fire(self):
        #fire bullet
        new_bullet = Bullet()
        new_bullet.rect = new_bullet.surf.get_rect(
            center=(
                player.rect.x + 15,
                player.rect.y
            )
        )
        bullets.add(new_bullet)
        all_sprites.add(new_bullet)

    def update_health_bar(self, index, health_bar):
        health_bar.update(index)
        if index <= 0:
            player.kill()
            return True
        return False
    
    def show_damages(self, screen):
        self.cp = self.surf.copy()
        self.cp.fill('red')
        screen.blit(self.cp, self.rect, None, pygame.BLEND_RGB_ADD)
            

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("Space Shooter/Assets/enemy_1.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.size = self.image.get_size()
        self.surf = pygame.transform.scale(self.image, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.surf.get_rect(
            center = (
                randint(0, SCREEN_WIDTH),
                0
            )
        )
        self.speed = randint(5, 8)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pygame.image.load("Space Shooter/Assets/bullet.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.size = self.image.get_size()
        self.surf = pygame.transform.scale(self.image, (int(self.size[0] // 2), int(self.size[1] // 2)))
        self.rect = self.surf.get_rect(
            center =(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 40
            )
        )
    
    def update(self):
        self.rect.move_ip(0, -7)
        if self.rect.top < -20: #sprite rect is larger than the laser itself
            self.kill()


class Health_bar(pygame.sprite.Sprite):
    def __init__(self):
        super(Health_bar, self).__init__()
        self.image_lst = []
        for i in range(6):
            self.image_lst.append(pygame.image.load(f"Space Shooter/Assets/health bar/{i}.png").convert())
        self.image = self.image_lst[5]
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.size = self.image.get_size()
        self.surf = pygame.transform.scale(self.image, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.surf.get_rect()

    def update(self, player_health):
        self.image = self.image_lst[player_health]
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.size = self.image.get_size()
        self.surf = pygame.transform.scale(self.image, (int(self.size[0] * 2), int(self.size[1] * 2)))
        self.rect = self.surf.get_rect()

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super(Meteor, self).__init__()
        self.image = pygame.image.load("Space Shooter/Assets/meteor.png").convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.size = self.image.get_size()
        self.surf = pygame.transform.scale(self.image, (int(self.size[0] * 5), int(self.size[1] * 5)))
        self.rect = self.surf.get_rect(
            center =(
                randint(0, SCREEN_WIDTH),
                randint(0, SCREEN_WIDTH // 2)
            )
        )
        self.speed = randint(1, 4)
        self.life = 4
        self.direction = randint(-4, 4) #to make meteors go diagonally
    
    def update(self):
        self.rect.move_ip(self.direction, self.speed)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


#display game over screen if player dead
def game_over():

    restart = False #controlling the loop to wait until player makes choice
    running = True #variable controling game loop non reachable inside function

    while not restart:

        #clean all sprites and display message
        all_sprites.empty()
        screen.fill((0, 0, 0))
        message_1 = font.render("GAME OVER", 0, (255, 255, 255))
        message_2 = font.render("Press SPACE to start again", 0, (255, 255, 255))
        screen.blit(message_1, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        screen.blit(message_2, (10, SCREEN_HEIGHT // 2 + 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #initiate new instances of player and health_bar if continue
                if event.key == K_SPACE:
                    player = Player()
                    health_bar = Health_bar()
                    all_sprites.add(player)
                    all_sprites.add(health_bar)
                    restart = True
                    return player, health_bar, running
                #quit game if wanted
                elif event.key == K_ESCAPE:
                    running = False
                    return running
            elif event.type == QUIT:
                running = False
                return running
                


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Event management
ADDENEMY = pygame.USEREVENT + 1
ADDMETEOR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, 400)
pygame.time.set_timer(ADDMETEOR, 1500)

# Sprites management
player = Player()
health_bar = Health_bar()
enemies = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(health_bar)

#Scrolling Background
background = pygame.image.load("Space Shooter/Assets/stars.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
scroll = 1
tiles = (SCREEN_HEIGHT // background.get_height()) + 1


font = pygame.font.Font("Space Shooter/Assets/monogram.ttf", size=30)

running = True

#GAME LOOP
while running:

    clock.tick(60)

    i = 0
    score_display = font.render("Score: " + str(player.score), 0, (255, 0, 0))

    #displaying sprites + scrolling
    while i < tiles:
        screen.blit(background, (0, background.get_height() * i + scroll))
        for entity in all_sprites:
            screen.blit(score_display, (SCREEN_WIDTH - 120, 0))
            screen.blit(entity.surf, entity.rect)
        i += 1
    scroll -=6
    if abs(scroll) > background.get_height():
        scroll = 0

    #event listening
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                player.fire()
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDMETEOR:
            new_meteor = Meteor()
            meteors.add(new_meteor)
            all_sprites.add(new_meteor)


    #move sprites
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    meteors.update()
    bullets.update()

    #check dead enemies
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, bullets, dokill=True):
            enemy.kill()
            player.score += 1
    
    #check if meteor damaged
    for meteor in meteors:
        if pygame.sprite.spritecollide(meteor, bullets, dokill=True):
            meteor.life -= 1
            if meteor.life <= 0:
                player.score += 3
                meteor.kill()

    #check if player damaged and draw game over screen if needed
    if pygame.sprite.spritecollide(player, enemies, dokill=True):
        player.health -= 1
        player.show_damages(screen)
        if player.update_health_bar(player.health, health_bar):
            player, health_bar, running = game_over()
    if pygame.sprite.spritecollide(player, meteors, dokill=True):
        player.health -= 2
        player.show_damages(screen)
        if player.update_health_bar(player.health, health_bar):
            player, health_bar, running = game_over()


    pygame.display.flip()
