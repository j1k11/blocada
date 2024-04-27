from pygame import *
from level import level

W,H = 1280,720
win = display.set_mode((W,H))
display.set_caption("Blockada")

level_width = len(level[0])*40
level_height = len(level)*40
c_count = 0

bg = transform.scale(image.load("images/bgr.png"),(W,H))

class Settings(sprite.Sprite):
    def __init__(self, x,y,w,h,speed,img):
        super().__init__()
        self.w = w 
        self.h = h
        self.speed = speed
        self.image = transform.scale(image.load(img),(self.w,self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))
        
class Player(Settings):
    def l_r(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
    def u_d(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
class Enemy(Settings):
    def __init__(self, x, y, w, h, speed, img, side):
        Settings.__init__(self,x, y, w, h, speed, img)
        self.side = side
    def update(self):
        global side
        if self.side == 'left':
            self.rect.x -= self.speed
        if self.side == 'right':
            self.rect.x += self.speed


class Camera():
    def __init__(self,camera_func,w,h):
        self.camera_func = camera_func
        self.state = Rect(0,0,w,h)
        
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    
    def update(self, turget):
        self.state = self.camera_func(self.state, turget.rect)
        
def camera_config(camera, target_rect):
    l,t,_,_ = target_rect
    _,_,w,h = camera
    l,t,= -l + W/2, -t + H/2
    l = min(0, l)
    t = min(0, t)
    l = max(-(camera.width - W),1)
    t = max(-(camera.height - H), t)
    t = min(0, t)
    
    return Rect(l,t,w,h)




#Це для IMAGES
background = 'images/bgr.png'
img_coin = 'images/coin.png'
img_door = 'images/door.png'
img_key = 'images/key.png'
img_chest_open = 'images/cst_open.png'
img_chest_close = 'images/cst_close.png'
img_cyborg = 'images/cyborg.png'
img_cyborg_r = 'images/cyborg_r.png'
img_stair = 'images/stair.png'
img_port = 'images/portal.png'
img_platform = 'images/platform.png'
img_nothing = 'images/nothing.png'
img_power = 'images/mana/png'
img_hero = 'images/sprite1.png'
img_hero_r = 'images/spirite1_r.png'

#Це для FONTS

font.init()

font1 = font.SysFont(('font/ariblk.ttf'), 200)
gname = font1.render('Blockada', True, (106, 90, 205), (250, 235, 215))

font2 = font.SysFont(('font/ariblk.ttf'), 60)
e_tap = font2.render('press (e)', True, (255, 0, 255))
k_need = font2.render('You need a key to open!', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))

font3 = font.SysFont(('font/calibrib.ttf'), 45)
wasd_b = font3.render('WASD - move buttons. You can only go up and down the stairs', True, (255, 0, 0))
space_b = font3.render('Space - shoot button. You are a wizard who only knows one spell', True, (255, 0, 0))
e_b = font3.render('E - interaction button. Open doors, collect keys, activate portals', True, (255, 0, 0))

font4 = font.SysFont(('font/ariblk.ttf'), 150)
done = font4.render('LEVEL DONE!', True, (0, 255, 0), (255, 100, 0))
lose = font4.render('YOU LOSE!', True, (255, 0, 0), (245, 222, 179))
pausa = font4.render('PAUSE', True, (255, 0, 0), (245, 222, 179))

#Це для SOUNDS

mixer.init()

fire_s = mixer.Sound('sounds/fire.ogg')
kick = mixer.Sound('sounds/kick.ogg')
k_up = mixer.Sound('sounds/k_coll.wav')
c_coll = mixer.Sound('sounds/c_coll.wav')
d_o = mixer.Sound('sounds/lock.wav')
tp = mixer.Sound('sounds/teleport.ogg')
click = mixer.Sound('sounds/click.wav')
cst_o = mixer.Sound('sounds/chest.wav')

#Це для OBJECTS
player = Player(300,650,50,50,5,img_hero)

enemy1 = Enemy(400,480,50,50,3,img_cyborg,'left')
enemy2 = Enemy(230,320,50,50,3,img_cyborg,'left')

door = Settings(1000,580,4,120,0,img_door)
key1 = Settings(160,350,50,20,0, img_key)
key2 = Settings(1500, 350,50,20,0,img_key)
portal = Settings(2700, 600,100,100,0, img_port)
chest = Settings(450,130,80,80,0, img_chest_close)

camera = Camera(camera_config,level_width,level_height)

#Це для groups
blocks_r = []
blocks_l = []
coins = []
stairs = []
platforms = []

items = sprite.Group()

#Це для GAME
win.blit(bg,(0,0))
x = y = 0
for r in level:
    for c in r:
        if c =="r":
            r1 = Settings(x,y,40,40,0,img_nothing)
            blocks_r.append(r1)
            items.add(r1)
        if c =="l":
            r2 = Settings(x,y,40,40,0,img_nothing)
            blocks_l.append(r2)
            items.add(r2)
        if c =='/':
            r3 = Settings(x,y-40,40,180,0,img_stair)
            stairs.append(r3)
            items.add(r3)
        if c =='°':
            r4 = Settings(x,y,40,40,0,img_coin)
            coins.append(r4)
            items.add(r4)
        if c == '-':
            r5 = Settings(x,y,40,40,0,img_platform)
            platforms.append(r5)
            items.add(r5)
        if c == '*':
            r6 = Settings(x,y,40,40,0, img_port)
            items.add(r6)
        if c == '>':
            r7 = Settings(x,y,40,40,0, img_chest_close)
            items.add(r7)
        x += 40
    y += 40
    x = 0

items.add(door)
items.add(key1)
items.add(key2)
items.add(portal)
items.add(chest)
items.add(enemy1)
items.add(enemy2)
items.add(player)

game = True

k_door = False
k_chest = False
o_chest = False


while game:
    win.blit(bg, (0,0))
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
    enemy1.update()
    enemy2.update()
    player.l_r()
    
    for r in blocks_r:
        if sprite.collide_rect(player, r):
            player.rect.x = r.rect.x + player.w
        if sprite.collide_rect(enemy1, r):
            enemy1.side = 'right'
            enemy1.image = transform.scale(image.load(img_cyborg), (enemy1.w, enemy1.h))
        if sprite.collide_rect(enemy2, r):
            enemy2.side = 'right'
            enemy2.image = transform.scale(image.load(img_cyborg_r), (enemy1.w, enemy2.h))
    for l in blocks_l:
        if sprite.collide_rect(player, l):
            player.rect.x = r.rect.x + player.w
        if sprite.collide_rect(enemy1, l):
            enemy1.side = 'left'
            enemy1.image = transform.scale(image.load(img_cyborg), (enemy1.w, enemy1.h))
        if sprite.collide_rect(enemy2, l):
            enemy2.side = 'left'
            enemy2.image = transform.scale(image.load(img_cyborg_r), (enemy1.w, enemy2.h))
    for c in coins:
        if sprite.collide_rect(player, c):
            coins.remove(c)
            c_coll.play()
            c_count += 1
            items.remove(c)
            
    for s in stairs:
        if sprite.collide_rect(player, s):
            player.u_d()
            if player.rect.y <= (s.rect.y - 40):
                player.rect.y = s.rect.y - 40
            if player.rect.y >= (s.rect.y + 130):
                player.rect.y = s.rect.y + 130
    
    enemy1.update()
    enemy2.update()
    camera.update(player)
    for i in items:
        win.blit(i.image, camera.apply(i))
    time.delay(15)       
    display.update()