import pygame as pg
from pygame import mixer
import random



#нулевой канал - фоновая музыка
#первый канал - ефекты
#второй канал - голоса
class DJ():
    def __init__(self):
      
        self.list_of_sounds={'punch':'sounds\\air_swing.wav',
                'slash':'sounds\\slash.wav',
                'magic_missle':'sounds\\magic.wav',
                'defense of king':"sounds\\[8 bit] Sabaton  - The Last Stand.wav",
                'challenge theme 1':'sounds\\[8 bit] Sabaton - Last Dying Breath.wav',
                'challenge theme 2':'sounds\\[8 bit] Sabaton - Rorkes Drift.wav'
                }
        self.ini=True
    def off(self):
        self.ini=False
    def on(self):
        self.ini=True
    def stop(self):
        mixer.music.stop()
    def play_random_infinity(self):
        list=['challenge theme 2','challenge theme 1']
        if self.ini:
            mixer.Channel(0).set_volume(0.3)
            Sound=mixer.Sound(self.list_of_sounds[random.choice(list)])
            mixer.Channel(0).play(Sound)
    def play_music(self,name):
         if self.ini:
            mixer.Channel(0).set_volume(0.3)
            mixer.Channel(0).play(mixer.Sound(self.list_of_sounds[name]))
    def play_effect(self,name):
        if self.ini:
            mixer.Channel(1).set_volume(0.5)
            Sound=mixer.Sound(self.list_of_sounds[name])
            mixer.Channel(1).play(Sound)

