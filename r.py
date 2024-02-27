import pygame

pygame.mixer.init()
pygame.init()

from math import sqrt
import numpy as np


# Maybe you can subclass the pygame.mixer.Sound and
# add the methods below to it..
class Fader(object):
    instances = []
    def __init__(self, fname, st):
        super(Fader, self).__init__()
        #assert isinstance(fname, basestring)
        self.sound = pygame.mixer.Sound(fname)
        self.increment = 0.1 # tweak for speed of effect!!
        self.next_vol = st # fade to 100 on start
        Fader.instances.append(self)

    def fade_to(self, new_vol):
        # you could change the increment here based on something..
        self.next_vol = new_vol

    @classmethod
    def update(cls):
        for inst in cls.instances:
            curr_volume = inst.sound.get_volume()

            if inst.next_vol > curr_volume:

                inst.sound.set_volume(min(curr_volume + inst.increment,1))
            elif inst.next_vol < curr_volume:

                inst.sound.set_volume(max(curr_volume - inst.increment,0))

trck="[2021.01.31] Messenger in Flames"
import time
v = Fader("sound/Cepheid/"+trck+"/vocal.flac",0)
m = Fader("sound/Cepheid/"+trck+"/minus.flac",1)
v.sound.play()
m.sound.play()


def draw_img(image, x, y, angle):
    rotated_image = pygame.transform.rotozoom(image, angle,1).convert_alpha()
    window.blit(rotated_image, rotated_image.get_rect(center=image.get_rect(topleft=(x, y)).center).topleft)


bpm=int(open("sound/Cepheid/"+trck+"/meta.txt","r").read().split("BPM")[0].split("\n")[-2])
print(trck,bpm)
v.sound.set_volume(0)

def minus():
    v.fade_to(0)
    m.fade_to(1)

def vocal():
    v.fade_to(1)
    m.fade_to(0)

#from keyboard import is_pressed as ip

clock = pygame.time.Clock()

c=0

window = pygame.display.set_mode((500, 500))
img = pygame.image.load("sound/Cepheid/"+trck+"/cover.jpg").convert_alpha()
img = pygame.transform.scale(img, (300, 300)) # image size

from colorthief import ColorThief
color_thief = ColorThief("sound/Cepheid/"+trck+"/cover.jpg")

dominant_color = color_thief.get_color(quality=1)

font = pygame.font.SysFont(None, 80)

dw=False

pr=time.time()

avg=0.1
while True:

    c+=1
    if abs(1-avg)<0.2:vocal()
    if abs(1-avg)>=0.2:minus()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or 1==1:
                d=(1/(time.time()-pr)*60)/bpm
                
                pr=time.time()
                avg=(5*avg+d)/6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e or 1==1:
                d=(1/(time.time()-pr)*60)/bpm
                pr=time.time()
                avg=(5*avg+d)/6
    Fader.update() # a call that will update all the faders..
    #print((1-avg)*100,end=" ")

    r=max(0,min(255,(   128-(1-avg)*100   )))
    g=max(0,min(255,(   255-abs(1-avg)*100   )))
    b=max(0,min(255,(   128+(1-avg)*100   )))

    imgt = font.render(str(-1*round((1-avg)*100,1)), True, (r,g,b))

    window.fill(dominant_color)
    window.blit(imgt, (20, 20))
    draw_img(img, 100, 120, (1-avg)*360)

    pygame.display.update()

    clock.tick(1200)
    #print([(round(i.sound.get_volume(),2),round(i.next_vol,2)) for i in Fader.instances],c%1000)