from pygame import mixer

#Background music
mixer.music.load("data/GM13.mp3")
mixer.music.play(-1)

#Shooting sound
def shooting_sound():
    bulllet_sound = mixer.Sound("data/shooting.mp3")
    bulllet_sound.play()




#Explosion sound
def explosion():
    explosion_sound = mixer.Sound("")
    explosion_sound.play()
