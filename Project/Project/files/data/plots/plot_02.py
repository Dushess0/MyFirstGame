import pygame as pg
import sprites
from settings import ICON_FOLDER

#king B

vec=pg.math.Vector2

radius=224
life_time=1000
call_key=0
steps=8
current_step=0
initiator=True
name="King B"
icon_path=ICON_FOLDER+"King B"+".png"



   
        
def move_in_time(start,end,actor,speed,dir,begin_time):
    start=start*1000
    end=end*1000
    now=pg.time.get_ticks()
    if  now>=start+begin_time and now<=end+begin_time:        
         
         actor.move(dir,speed)        
   
       
def call_on_second(actor,time_pos,begin_time,TRIGER,range):
     now=pg.time.get_ticks()
     if pg.time.get_ticks()>=begin_time+time_pos*1000 and pg.time.get_ticks()<=begin_time+range*1000+time_pos*1000:
        actor.call(TRIGER)
def show_words_in_pos(string,timer,actor,pos,time_pos,begin_time):
     now=pg.time.get_ticks()
     if pg.time.get_ticks()>=begin_time+time_pos*1000 and pg.time.get_ticks()<=begin_time+timer*1000+time_pos*1000:
       sprites.Floating_number(actor.game,pos.x,pos.y,string,"words",timer)

def execute(actor,begin_time):   
     
     
     actor.show_words_on_second("Hello!",1,1,begin_time)             
     actor.show_words_on_second("Are you cleared exit?",1,4,begin_time) 
     actor.game.player_1.say_words("Yes",1,7,begin_time)
     actor.show_words_on_second("We need to go, soon it will be hot here!",2,9,begin_time)  
     
     move_in_time(12,15,actor,2,"left",begin_time)
     actor.show_words_on_second("I need to tie shoelaces",2,17,begin_time)   
     actor.game.player_1.say_words("You need to go. I will stop them!",1,29,begin_time)
     actor.game.player_1.say_words("Hrrrrrrr.  ***fell asleep*** ",2,35,begin_time)
     actor.show_words_on_second("",2,9,begin_time)  
     call_on_second(actor,17,begin_time,1,1)
     show_words_in_pos("#UNNAMED GAME(TEMPORARY)#",100,actor,vec(actor.pos.x+200,actor.pos.y-100),48,begin_time)
     show_words_in_pos("WRITTEN by Ilya Bannitsyn",100,actor,vec(actor.pos.x+1400,actor.pos.y-100),48,begin_time)
     show_words_in_pos("Special thanks for all testers!",100,actor,vec(actor.pos.x+2200,actor.pos.y-100),48,begin_time)
     

     

  
