#B
import pygame as pg
import sprites
from settings import ICON_FOLDER
radius=-1
life_time=60
call_key=1
shots=1
name="Guard B"
icon_path=ICON_FOLDER+"Guards"+".png"
vec=pg.math.Vector2
def move_in_time(start,end,actor,speed,dir,begin_time):
    start=start*1000
    end=end*1000
    now=pg.time.get_ticks()
    if  now>=start+begin_time and now<=end+begin_time:        
         
         actor.move(dir,speed)        
   
   

def shoot_on_second(damage,shell_type,pos,actor,time_pos,begin_time,range):
     now=pg.time.get_ticks()
     if actor.shots>0:
         if pg.time.get_ticks()>=begin_time+time_pos*1000 and pg.time.get_ticks()<=begin_time+range*1000+time_pos*1000:
           actor.shots-=1
      
           sprites.Attack(actor.game,vec(actor.pos.x,actor.pos.y+20),actor.shoot_rot,damage,shell_type,"arrow",'heroes',w=actor.rect.width,h=actor.rect.height,isStunning=True)
           hits=pg.sprite.groupcollide(actor.game.heroes,actor.game.attacks,False,False)
           if hits:
            for hero,attacks in hits.items():
               hero.isStunned=True

def execute(actor,begin_time):   
    move_in_time(0,6,actor,3.4,"left",begin_time)
    shoot_on_second(0,"magical",actor.pos,actor,17,begin_time,0.3)
    
     

  
