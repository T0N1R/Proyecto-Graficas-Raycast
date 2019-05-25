import pygame
from math import pi, cos, sin, atan2

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

pygame.mixer.music.load("Chala.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 255, 255)


wall1 = pygame.image.load('./cellSaga1.png')
wall2 = pygame.image.load('./namek1.png')
wall3 = pygame.image.load('./namek2.png')
wall4 = pygame.image.load('./friezaArc.png')
wall5 = pygame.image.load('./friezaSaga1.png')
wall6 = pygame.image.load('./friezaSaga2.png')
wall7 = pygame.image.load('./friezaSaga3.png')
wall8 = pygame.image.load('./friezaSaga4.png')
wall9 = pygame.image.load('./friezaSaga5.png')
wall10 = pygame.image.load('./friezaSaga7.png')
wall11 = pygame.image.load('./friezaSaga8.png')
wall12 = pygame.image.load('./cinta.png')
wall13 = pygame.image.load('./cellSaga2.png')
wall14 = pygame.image.load('./cellSaga3.png')
wall15 = pygame.image.load('./cellSaga4.png')
wall16 = pygame.image.load('./cellSaga5.png')
wall17 = pygame.image.load('./cellSaga6.png')
wall18 = pygame.image.load('./cellSaga9.png')
wall19 = pygame.image.load('./buuSaga1.png')
wall20 = pygame.image.load('./buuSaga2.png')
wall21 = pygame.image.load('./buuSaga3.png')
wall22 = pygame.image.load('./buuSaga4.png')
wall23 = pygame.image.load('./buuSaga5.png')
wall24 = pygame.image.load('./buuSaga6.png')
wall25 = pygame.image.load('./tierra1.png')
wall26 = pygame.image.load('./tierra2.png')
wall27 = pygame.image.load('./espacio1.png')
wall28 = pygame.image.load('./espacio2.png')




textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5,
  "6": wall6,
  "7": wall7,
  "8": wall8,
  "9": wall9,
  "0": wall10,
  "q": wall11,
  "A": wall12,
  "B": wall13,
  "C": wall14,
  "D": wall15,
  "E": wall16,
  "F": wall17,
  "G": wall18,
  "H": wall19,
  "I": wall20,
  "J": wall21,
  "K": wall22,
  "L": wall23,
  "M": wall24,
  "N": wall25,
  "O": wall26,
  "P": wall27,
  "Q": wall28
}

hand = pygame.image.load('./player.png')

enemies = [
  {
    "x": 440,
    "y": 130,
    "texture": pygame.image.load('./goku1.png')
  },
  {
    "x": 440,
    "y": 85,
    "texture": pygame.image.load('./frieza.png')
    },
  {
    "x": 300,
    "y": 400,
    "texture": pygame.image.load('./cell.png')
    },
  {
    "x":267,
    "y":400,
    "texture": pygame.image.load('./kaka.png')
    },
  {
    "x":65,
    "y":375,
    "texture": pygame.image.load('./buu.png')
    },
  {
    "x":65,
    "y":340,
    "texture": pygame.image.load('./goku3.png')
    }
]

class Raycaster(object):
  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = 100
    self.player = {
      "x": self.blocksize + 20,
      "y": self.blocksize + 20,
      "a": pi/3,
      "fov": pi/3
    }
    self.map = []
    self.zbuffer = [-float('inf') for z in range(0, 500)]
    # self.clear()

  def clear(self):
    for x in range(self.width):
      for y in range(self.height):
        r = int((x/self.width)*255) if x/self.width < 1 else 1
        g = int((y/self.height)*255) if y/self.height < 1 else 1
        b = 0
        color = (r, g, b)
        self.point(x, y, color)

  def point(self, x, y, c = None):
    screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + 50):
      for cy in range(y, y + 50):
        tx = int((cx - x)*128 / 50)
        ty = int((cy - y)*128 / 50)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + d*cos(a)
      y = self.player["y"] + d*sin(a)

      i = int(x/50)
      j = int(y/50)

      if self.map[j][i] != ' ':
        hitx = x - i*50
        hity = y - j*50

        if 1 < hitx < 49:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * 128 / 50)

        return d, self.map[j][i], tx


      d += 1

  def draw_stake(self, x, h, texture, tx):
    start = int(250 - h/2)
    end = int(250 + h/2)
    for y in range(start, end):
      ty = int(((y - start)*128)/(end - start))
      c = texture.get_at((tx, ty))
      self.point(x, y, c)

  def draw_sprite(self, sprite):
    sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])   # why atan2? https://stackoverflow.com/a/12011762

    sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
    sprite_size = (500/sprite_d) * 30

    sprite_x = 500 + (sprite_a - self.player["a"])*500/self.player["fov"] + 250 - sprite_size/2
    sprite_y = 250 - sprite_size/2

    sprite_x = int(sprite_x)
    sprite_y = int(sprite_y)
    sprite_size = int(sprite_size)

    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
          tx = int((x - sprite_x) * 148/sprite_size)
          ty = int((y - sprite_y) * 128/sprite_size)
          c = sprite["texture"].get_at((tx, ty))
          #print(c)
          if c != (0, 255, 80, 255):
            self.point(x, y, c)
            self.zbuffer[x - 500] = sprite_d

  def draw_player(self, xi, yi, w = 256, h = 256):
    for x in range(xi, xi + w):
      for y in range(yi, yi + h):
        tx = int((x - xi) * 32/w)
        ty = int((y - yi) * 32/h)
        c = hand.get_at((tx, ty))
        if c != (152, 0, 136, 255):
          self.point(x, y, c)

  def render(self):
    for x in range(0, 500, 50):
      for y in range(0, 500, 50):
        i = int(x/50)
        j = int(y/50)
        if self.map[j][i] != ' ':
          self.draw_rectangle(x, y, textures[self.map[j][i]])

    self.point(self.player["x"], self.player["y"], (255, 255, 255))

    for i in range(0, 500):
      self.point(500, i, (0, 0, 0))
      self.point(501, i, (0, 0, 0))
      self.point(499, i, (0, 0, 0))

    for i in range(0, 500):
      a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/500
      d, c, tx = self.cast_ray(a)
      x = 500 + i
      h = 500/(d*cos(a-self.player["a"])) * 70
      self.draw_stake(x, h, textures[c], tx)
      self.zbuffer[i] = d

    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], (0, 0, 0))
      self.draw_sprite(enemy)

    self.draw_player(1000 - 256 - 128, 500 - 256)

pygame.init()
screen = pygame.display.set_mode((1000, 500), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN|pygame.HWSURFACE)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./map.txt')

c = 0
while True:
  screen.fill((113, 113, 113))
  r.render()

  for e in pygame.event.get():
    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
      exit(0)
    if e.type == pygame.KEYDOWN:
      if e.key == pygame.K_a:
        r.player["a"] -= pi/10
        print(r.player["a"])
      elif e.key == pygame.K_d:
        r.player["a"] += pi/10

      elif e.key == pygame.K_RIGHT:
        r.player["x"] += 10
      elif e.key == pygame.K_LEFT:
        r.player["x"] -= 10
        
      elif e.key == pygame.K_UP:
        try:
          r.player["y"] += int(sin(r.player["a"]) * 10)
          r.player["x"] += int(cos(r.player["a"]) * 10)
        except:
          r.player["y"] -= int(sin(r.player["a"]) * 1)
          r.player["x"] -= int(cos(r.player["a"]) * 1)
        
      elif e.key == pygame.K_DOWN:
        try:
          r.player["y"] -= int(sin(r.player["a"]) * 10)
          r.player["x"] -= int(cos(r.player["a"]) * 10)
        except:
          r.player["y"] += int(sin(r.player["a"]) * 1)
          r.player["x"] += int(cos(r.player["a"]) * 1)

      if e.key == pygame.K_f:
        if screen.get_flags() and pygame.FULLSCREEN:
            pygame.display.set_mode((1000, 500))
        else:
            pygame.display.set_mode((1000, 500),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN)

  pygame.display.flip()
