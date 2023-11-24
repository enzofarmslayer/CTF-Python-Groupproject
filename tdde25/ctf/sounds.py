from pygame import mixer

#Background music
mixer.music.load("data/GM13.mp3")
mixer.music.play(-1)

#Shooting sound
def shooting_sound():
    bulllet_sound = mixer.Sound("data/Shooting.wav")
    bulllet_sound.play()


#Explosion sound
def explosion():
    explosion_sound = mixer.Sound("data/Explosion.wav")
    explosion_sound.play()


def captured_the_flag():
    flag_sound = mixer.Sound("")
    flag_sound.play()




