from random import randint
from time import time as timer
from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Permainan Shooter Favoritku!')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
window.blit(background, (0, 0))
font.init()
font = font.Font(None, 36)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
missed_enemies = 0
num_fired = 0
reload_time = False
last_reload_time = 0
bullets = sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, image_width=65, image_height=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (image_width, image_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, image_width=5, image_height=15):
        super().__init__(player_image, player_x, player_y, player_speed, image_width, image_height)
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        self.score = 0
        super().__init__(player_image, player_x, player_y, player_speed)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)
        mixer.Sound('fire.ogg').play()

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.asteroid_kill = 0
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(40, 660)
            global missed_enemies
            missed_enemies += 1

player = Player('rocket.png', 320, 430, 15)
def gererate_enemies(number=5):
    for i in range(number):
        enemy = Enemy('ufo.png', randint(40, 660), 0, randint(1, 4))
        enemies.add(enemy)
    for i in range(2):
        asteroid = Enemy('asteroid.png', randint(40, 660), 0, randint(1, 4))
        asteroids.add(asteroid)
gererate_enemies(5)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
            if e.key == K_r:
                finish = False
                missed_enemies = 0
                player.score = 0
                bullets.empty()
                enemies.empty()
                gererate_enemies(5)
                mixer.music.play()
            if e.key == K_SPACE:
                if num_fired < 5 and reload_time == False:
                       num_fired = num_fired + 1
                       player.fire()
                if num_fired >= 5 and reload_time == False : #if the player fired 5 shots
                       last_reload_time = timer() #record time when this happened
                       reload_time = True #set the reload flag

    if not finish:
        window.blit(background,(0,0))
        score_text = font.render(f'Score: {player.score}', True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        missed_enemies_text = font.render(f'Missed Enemies: {missed_enemies}', True, (255, 255, 255))
        window.blit(missed_enemies_text, (10, 50))
        player.update()
        bullets.update()
        player.reset()
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()

        #reload
        if reload_time == True:
            now_time = timer() #read time
        
            if now_time - last_reload_time < 3: #before 3 seconds are over, display reload message
                reload = font.render('Wait, reload...', 1, (255, 255, 0))
                window.blit(reload, (260, 360))
            else:
                num_fired = 0   #set the bullets counter to zero
                reload_time = False #reset the reload flag

        is_asteroid_fired = sprite.groupcollide(bullets, asteroids, True, False)
        if missed_enemies >= 3 or sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            lose_text = font.render('You Lose!', True, (255, 0, 0))
            window.blit(lose_text, (300, 200))
            lose_text = font.render('Pencet R untuk mengulang', True, (0, 255, 0))
            # lose_background = transform.scale(image.load('lose.jpg'), (700, 500))
            # window.blit(lose_background, (0, 0))
            window.blit(lose_text, (200, 450))
            mixer.music.stop()
        is_fired = sprite.groupcollide(bullets, enemies, True, True)
        for bullet in is_fired:
            player.score += 1
            enemy = Enemy('ufo.png', randint(40, 660), 0, randint(1, 4))
            enemies.add(enemy)
        if player.score >= 10:
            finish = True
            lose_text = font.render('You Win!', True, (0, 255, 0))
            window.blit(lose_text, (300, 200))
            lose_text = font.render('Pencet R untuk mengulang', True, (0, 255, 0))
            # winner_background = transform.scale(image.load('win.jpg'), (700, 500))
            # window.blit(winner_background, (0, 0))
            window.blit(lose_text, (200, 450))
            mixer.music.stop()
        display.update()
    time.delay(50)