import pygame
import os
import random
import sys
import math

pygame.font.init()
pygame.mixer.init()
pygame.init()

VELOCITY = 10 # speed of player
SPEED_BULLET = 5 #speedof bullet
MAX_BULLETS = 10 # maximum no. of bullets


WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BG_COLOR = ( 50,50,50)

ENEMY_WIDTH , ENEMY_HEIGHT = 40 , 40
WEIDTH_SHIP , HEIGHT_SHIP = 70,70
WEIDTH , HEIGHT = 500,500
SCREEN = pygame.display.set_mode((WEIDTH,HEIGHT))
Caption = pygame.display.set_caption(("space shooter made by kunal"))

FPS = 30
colock = pygame.time.Clock()

SHOOT_SOUND = pygame.mixer.Sound(os.path.join("assets/Gun+Silencer.mp3"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets/Grenade+1.mp3"))
GAME_OVER = pygame.mixer.Sound(os.path.join("assets/mixkit-arcade-retro-game-over-213.wav"))


#-------USER_EVENT------#
SHIP_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

#___________SCORING_SYS>.________________#
SCORE = 0
SCORE_inc = 1
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

def draw_score(SCORE_FONT ,SCORE , SCREEN):
    score_text = SCORE_FONT.render(f'Score: {SCORE}', True, (255, 255, 255))
    SCREEN.blit (score_text , (200,50))
    pygame.display.update()

#__________ENEMY__________#

ENEMY_SHIP_IMAGE = pygame.image.load(os.path.join("assets/spaceship_yellow.png"))
SIZE_ENEMY = pygame.transform.scale( ENEMY_SHIP_IMAGE , (50 , 50 )) 

class Enemy_player(pygame.sprite.Sprite):  # making sprites using classes and object
 
    def __init__(self , x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = SIZE_ENEMY   
        self.rect = self.image.get_rect()
        self.rect.center = ( x ,y )  
        self.speed = random.randint(1,3)  # it is used to give different speed       
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500 - HEIGHT_SHIP/2: 
            GAME_OVER.play()
            draw_winner(winner_text)
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            
        for BUllet in YELLOW_bullets:
            if self.rect.colliderect(BUllet):
                self.rect.y = -300
                HIT_SOUND.play()
                                         
        if self.rect.colliderect(SHIP) :
            GAME_OVER.play()
            draw_winner(winner_text)
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()    
      
#_______ALL_SPRITES_________#
all_sprites = pygame.sprite.Group()

enemy = Enemy_player(250,-105)
enemy_2 = Enemy_player(150,-200)
enemy_3 = Enemy_player(350,-0)
enemy_4 = Enemy_player(50,-150)
enemy_5 = Enemy_player(450,-250)

all_sprites.add(enemy)
all_sprites.add(enemy_2)
all_sprites.add(enemy_3)
all_sprites.add(enemy_4)
all_sprites.add(enemy_5)

#________PLAYER_______#

RED_PLAYER = pygame.image.load(os.path.join("assets/spaceship_red.png")) # load players image
SIZE_IMAGE = pygame.transform.scale(RED_PLAYER , (WEIDTH_SHIP,HEIGHT_SHIP) ) # give  dimension
ROTATE_IMAGE = pygame.transform.rotate(SIZE_IMAGE, (180)) # rotating image
SHIP = pygame.Rect(220,425 , WEIDTH_SHIP,HEIGHT_SHIP) # coordinates of player ship

def draw_PLAYER_SHIP(SHIP, ROTATE_IMAGE ):
    
    SCREEN.blit(ROTATE_IMAGE , (SHIP.x,SHIP.y)) # putting player image to  the screen

#____________BULLET______________#
def PLAYER_BULLET(YELLOW_bullets):
    for BUllet in YELLOW_bullets :
        pygame.draw.rect(SCREEN, YELLOW, BUllet,10,5)

    for BUllet in YELLOW_bullets :
            BUllet.y -= SPEED_BULLET
    for BUllet in YELLOW_bullets : 
        if BUllet.y < 0 :
            YELLOW_bullets.remove(BUllet)

            
#____________WINNER______________#
winner_text = "GAME OVER"
WINNER_FONT  = pygame.font.SysFont('comcsans' , 75)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text , 1 , YELLOW)
    SCREEN.blit(draw_text, (100,250))
    pygame.display.update()
    pygame.time.delay(5000)
          
#________MAIN_FUUNCTION__________#

YELLOW_bullets = []  
runing = True
while runing:
    colock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
            pygame.quit()
            
         #_______BULLET______#  
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE and len(YELLOW_bullets) < MAX_BULLETS:
                BUllet = pygame.Rect(SHIP.x + WEIDTH_SHIP/2 - 3 , SHIP.y  , 5,10) # 10,5 is weidth or heidht of bullet                
                YELLOW_bullets.append(BUllet)
                SHOOT_SOUND.play()
  
        button_preesed = pygame.key.get_pressed()
            
        if button_preesed[pygame.K_a] and SHIP.x > 0:
            SHIP.x -= VELOCITY
        if button_preesed[pygame.K_d] and SHIP.x < WEIDTH - 70 :
            SHIP.x += VELOCITY
        if button_preesed[pygame.K_w] and SHIP.y > 0 :
            SHIP.y -= VELOCITY
        if button_preesed[pygame.K_s] and SHIP.y < HEIGHT - 70 :
            SHIP.y += VELOCITY

    for BUllet in YELLOW_bullets:
        if enemy.rect.colliderect(BUllet):
            SCORE += SCORE_inc
        elif enemy_2.rect.colliderect(BUllet):
            SCORE += SCORE_inc
        elif enemy_3.rect.colliderect(BUllet):
            SCORE += SCORE_inc    
        elif enemy_4.rect.colliderect(BUllet):
            SCORE += SCORE_inc               
        elif enemy_5.rect.colliderect(BUllet):
            SCORE += SCORE_inc    
    
    SCREEN.fill(BG_COLOR)
    all_sprites.draw(SCREEN)
     
    draw_PLAYER_SHIP(SHIP ,ROTATE_IMAGE )
    draw_score(SCORE_FONT , SCORE , SCREEN)
    
    all_sprites.update()
    
    PLAYER_BULLET(YELLOW_bullets)
   
    pygame.display.flip()

#### IMPORTANT POINTS ###
# always connect/indent pygame.display.update with while loop  