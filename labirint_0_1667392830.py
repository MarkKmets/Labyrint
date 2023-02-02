#підключаємо модуль
from pygame import *
#змінні з кольором
green=(0,255,0)
#створення та іменування вікна
width=700
height=500
window=display.set_mode((width,height))
display.set_caption('Лабіринт')
#змінні прапорці
finish = False
play=True
#класи
class GameSprite(sprite.Sprite):
    def __init__(self,x,y,width,height,name):
        super().__init__()
        self.image=transform.scale(image.load(name),(width,height))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,x,y,width,height,x_speed,y_speed,name):
        GameSprite.__init__(self,x,y,width,height,name)
        self.x_speed=x_speed
        self.y_speed=y_speed
    def update(self):
        if ghost.rect.x <= width-80 and ghost.x_speed > 0 or ghost.rect.x >= 0 and ghost.x_speed < 0:
            self.rect.x += self.x_speed
        touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if ghost.rect.y <= height-80 and ghost.y_speed > 0 or ghost.rect.y >= 0 and ghost.y_speed < 0:
            self.rect.y += self.y_speed
        touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for p in touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

#створення гравця
picture=GameSprite(0,0,700,500,"display.jpg")       
ghost=Player(10,400,70,70,0,0,"ghost.png")
enemy=GameSprite(width - 200, 180, 40, 100,'enemy.png')
final=GameSprite(width - 85, height - 100, 80, 80,'flag.png')

#створення стін
walls=sprite.Group()
wall1=GameSprite(370,250 ,50,300,"wall1.png")
wall2=GameSprite(0,height/2,300,50,"wall2.png")
wall3=GameSprite(0,100,400,50,"wall2.png")
wall4=GameSprite(400,100,400,50,"wall2.png")
walls.add(wall1)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
#основний ігровий цикл
while play: 
    #обробка подій
    for e in event.get():
        if e.type == QUIT:
            play=False
        elif e.type==KEYDOWN:
            if e.key==K_LEFT:
                ghost.x_speed=-5
            elif e.key==K_RIGHT:
                ghost.x_speed=5
            elif e.key==K_UP:
                ghost.y_speed=-5
            elif e.key==K_DOWN:
                ghost.y_speed=5
        elif e.type==KEYUP:
            if e.key==K_LEFT:
                ghost.x_speed=0
            elif e.key==K_RIGHT:
                ghost.x_speed=0
            elif e.key==K_UP:
                ghost.y_speed=0
            elif e.key==K_DOWN:
                ghost.y_speed=0
    if not finish:
        picture.draw()
        walls.draw(window)
    #малювання ворога та персонажа
    ghost.draw()
    final.draw()
    enemy.draw()
    #підключення функції руху персонажа
    ghost.update()

    if sprite.collide_rect(ghost, enemy):
        finish = True
        # обчислюємо ставлення
        img = image.load('game_over.jpg')
        d = img.get_width() // img.get_height()
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (height * d, height)), (90, 0))

    if sprite.collide_rect(ghost, final):
        finish = True
        img = image.load('winner.jpg')
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (width, height)), (0, 0))
    #оновлення сцени
    time.delay(30)
    display.update()
display.update()
