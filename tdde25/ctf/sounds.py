import pygame
from pygame import mixer


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()


# Preloading of all sounds
mixer.music.load("data/GM13.mp3")
bulllet_sound = mixer.Sound("data/Shooting.wav")
explosion_sound = mixer.Sound("data/Explosion.wav")
flag_sound = mixer.Sound("data/Victor_sound.wav")
wooden_box = mixer.Sound("data/wood.wav")
# Background music
mixer.music.play(-1)


# Shooting sound
def shooting_sound():
    bulllet_sound.play()


# Explosion sound
def explosion():
    explosion_sound.play()


# "Flag capture" sound
def captured_the_flag():
    flag_sound.play()


def wood_box():
    wooden_box.play()
