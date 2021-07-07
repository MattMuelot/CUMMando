import os
import pygame
import time
import random

pygame.font.init()
font_color = (0, 0, 0)

# Load audio files

pygame.mixer.init(buffer=512)
moan = pygame.mixer.Sound(os.path.join('Assets', 'ooh.ogg'))
pygame.mixer.Sound.set_volume(moan, .9)
shemoan = pygame.mixer.Sound(os.path.join('Assets', 'shemoan.ogg'))
mcgavin = pygame.mixer.Sound(os.path.join('Assets', 'mcgavin.ogg'))
sheyell = pygame.mixer.Sound(os.path.join('Assets', 'sheyell.ogg'))
nutmed = pygame.mixer.Sound(os.path.join('Assets', 'nut.ogg'))
khanmed = pygame.mixer.Sound(os.path.join('Assets', 'khan.ogg'))
pygame.mixer.Sound.set_volume(nutmed, .4)
pygame.mixer.Sound.set_volume(mcgavin, .4)
pygame.mixer.Sound.set_volume(khanmed, .4)
pygame.mixer.Sound.set_volume(sheyell, .5)
twins = pygame.mixer.Sound(os.path.join('Assets', 'twins.ogg'))
twins.set_volume(.4)


width, height = 900, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('CUMMando')

# Load PNG Assets

PENIS = pygame.image.load(os.path.join('Assets', 'penile.png')).convert_alpha()
BACKGROUND = pygame.image.load(os.path.join('Assets', 'gamebg.png')).convert_alpha()
SPERM = pygame.image.load(os.path.join('Assets', 'sperm.png')).convert_alpha()
VAG = pygame.image.load(os.path.join('Assets', 'vag.png')).convert_alpha()
MCG = pygame.image.load(os.path.join('Assets', 'shootermedal.png')).convert_alpha()
NUT = pygame.image.load(os.path.join('Assets', 'nutmedal.png')).convert_alpha()
KHAN = pygame.image.load(os.path.join('Assets', 'khan.png')).convert_alpha()
MENUBG = pygame.image.load(os.path.join('Assets', 'menubg.png')).convert_alpha()
PMENU = pygame.image.load(os.path.join('Assets', 'pausemenu.png')).convert_alpha()
SMENU = pygame.image.load(os.path.join('Assets', 'settings.png')).convert_alpha()


class Mover:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.score = 0
        self.lives = 3
        self.sperm_image = None
        self.mover_image = None
        self.semen = []
        self.cool_down_counter = 0
        self.medals = []
        self.medals_awarded = []

    def draw(self, window):
        window.blit(self.mover_image, (self.x, self.y))
        for s in self.semen:
            s.draw(window)

    def move_cum(self, vel, objs):
        for s in self.semen:
            s.move(vel)
            if s.off_screen(0):
                self.semen.remove(s)
            else:
                for obj in objs:
                    if s.collision(obj):
                        objs.remove(obj)
                        try:
                            self.semen.pop()
                        except Exception:
                            twins.play()
                        self.score += 1
                        shemoan.play()

    def get_width(self):
        return self.mover_image.get_width()

    def get_height(self):
        return self.mover_image.get_height()

    def shoot(self):
        cum = Cummy(self.x + 47, self.y - 50, self.sperm_image)
        self.semen.append(cum)

    def award_medals(self, medal, location):
        self.medals.append([medal, False, location])

    def draw_medals(self, window):
        for m in self.medals_awarded:
            if m == 'nut':
                window.blit(pygame.transform.scale(NUT, (75, 75)), (825, 400))
            if m == 'shooter':
                window.blit(pygame.transform.scale(MCG, (75, 75)), (775, 400))
            if m == 'testicle':
                window.blit(pygame.transform.scale(KHAN, (75, 75)), (725, 400))


class Cummy:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y -= vel

    def off_screen(self, h):
        return self.y <= h and self.y >= 0

    def collision(self, obj):
        return collide(self, obj)


class Dick(Mover):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.mover_image = PENIS
        self.sperm_image = SPERM
        self.mask = pygame.mask.from_surface(self.mover_image)
        self.max_health = health


class Pussy(Mover):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.mover_image = VAG
        self.mask = pygame.mask.from_surface(self.mover_image)

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


clock = pygame.time.Clock()


def main():
    pygame.mixer.music.load(os.path.join('Assets', 'lovegun.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.1)
    running = True
    FPS = 60
    player_vel = 10
    dick = Dick(350, 400)
    main_font = pygame.font.SysFont('comicsans', 35)
    pussies = []
    wave_length = 10
    enemy_vel = 1

    def redraw_window():
        screen.blit(BACKGROUND, (0, 0))  # Draw background
        score_label = main_font.render(f'Score: {score}', True, font_color)
        lives_label = main_font.render(f'Lives: {lives}', True, font_color)
        screen.blit(score_label, (0, 475))
        screen.blit(lives_label, (800, 475))
        for m in medals:
            if m[0] == 'nut' and m[1] is False:
                dick.medals_awarded.append('nut')
            if m[0] == 'shooter' and m[1] is False:
                dick.medals_awarded.append('shooter')
            if m[0] == 'testicle' and m[1] is False:
                dick.medals_awarded.append('testicle')
        dick.draw(screen)
        dick.draw_medals(screen)
        for puss in pussies:
            puss.draw(screen)
        pygame.display.update()

    while running:
        score = dick.score
        lives = dick.lives
        medals = []
        clock.tick(FPS)
        if score == 50:
            if 'nut' not in dick.medals_awarded:
                medals.append(['nut', False])
                nutmed.play()
        if score == 100:
            if 'shooter' not in dick.medals_awarded:
                medals.append(['shooter', False])
                mcgavin.play()
        if score == 200:
            if 'testicle' not in dick.medals_awarded:
                medals.append(['testicle', False])
                khanmed.play()
        if len(pussies) == 0:
            wave_length += 10
            for p in range(wave_length):
                pussy = Pussy(random.randint(0, 800), random.randint(-1500, -100))
                pussies.append(pussy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    moan.play()
                    dick.shoot()
                if event.key == pygame.K_p:
                    result = pause_game()
                    if result is False:
                        return False
                    else:
                        pygame.mixer.music.load(os.path.join('Assets', 'lovegun.mp3'))
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(.1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and dick.x - player_vel > 0:  # LEFT
            dick.x -= player_vel
        if keys[pygame.K_d] and dick.x + player_vel < 800:  # RIGHT
            dick.x += player_vel

        for p in pussies[:]:
            p.move(enemy_vel)
            if p.y + p.get_height() > height:
                pussies.remove(p)
                sheyell.play()
                dick.lives -= 1
                if dick.lives < 1:
                    with open('scores.txt', 'a') as f:
                        f.write(f'You scored: {score}\n')
                    running = False
        dick.move_cum(10, pussies)
        redraw_window()


def pause_game():
    paused = True
    pygame.mixer.music.load(os.path.join('Assets', 'bread.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.1)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    result = main()
                    if result is False:
                        return False
                    else:
                        main_menu()
        screen.blit(PMENU, (0, 0))
        pygame.display.update()
        clock.tick(30)


def settings_screen():
    running = True
    while running:
        screen.blit(SMENU, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    main_menu()


def main_menu():
    pygame.mixer.music.load(os.path.join('Assets', 'bread.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.1)
    running = True
    title_font = pygame.font.SysFont('comicsans', 50)
    while running:
        screen.blit(MENUBG, (0, 0))
        title_label = title_font.render('Press Space To Begin...', True, (255, 255, 255))
        setting_label = title_font.render('Press S To View Settings...', True, (255, 255, 255))
        screen.blit(title_label, (275, 370))
        screen.blit(setting_label, (275, 425))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    result = main()
                    if result is False:
                        running = False
                    else:
                        # running = False
                        pygame.mixer.init(buffer=512)
                        pygame.mixer.music.load(os.path.join('Assets', 'bread.mp3'))
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(.1)
                elif event.key == pygame.K_s:
                    result = settings_screen()
                    if result is False:
                        running = False
                    else:
                        pass


    pygame.quit()
    quit()


main_menu()
