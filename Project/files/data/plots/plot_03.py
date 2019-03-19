#A
import pygame as pg
import sprites
from settings import ICON_FOLDER

radius=-1
life_time=60
call_key=1
name="Guard A"
icon_path=ICON_FOLDER+"Guards"+".png"
from settings import PLAYER_ACC
vec=pg.math.Vector2
def move_in_time(start,end,actor,speed,dir,begin_time):
    start=start*1000
    end=end*1000
    now=pg.time.get_ticks()
    if  now>=start+begin_time and now<=end+begin_time:        
         
         actor.move(dir,speed)        
   
  
def move_player_on_second(hero,dir,start,end,begin_time):
    if dir=='right':
        speed_k=1
    elif dir=="left":
        speed_k=-1
    start=start*1000
    end=end*1000
    now=pg.time.get_ticks()
    if  now>=start+begin_time and now<=end+begin_time:        
         self.acc.x = PLAYER_ACC* speed_k                        
       
def execute(actor,begin_time):  
    
     move_in_time(0,6,actor,3.4,"left",begin_time)

     actor.show_words_on_second("Halt!",1,7,begin_time)

     actor.show_words_on_second("You are aressted!",2,10,begin_time)

     actor.show_words_on_second("Arrest king and this guy",2,20,begin_time)
     

  
