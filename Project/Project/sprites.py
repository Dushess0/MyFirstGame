import pygame as pg
import basic
from settings import *
import json
import math
import random
import HUD
import importlib.util

import os
from language_manager import language_text as get_text
import language_manager
vec=pg.math.Vector2

def give_named_item_code(name,game):
    i=0
    while True:
            with open(items_file) as file:
                        data=json.load(file)
            i+=1
            item=Item(game,0,0,i)
            item.kill()
            if item.name==name:
                break
            
    return item
class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.heroes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game  
        self.image=pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(BLACK)
        self.current_frame=0
        self.last_update=0
        self.can_climb=False
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.vel=vec(0,0)
        self.pos=vec(x,y)
        
        self.acc = vec(0, 0)

    def get_keys(self):
        keys = pg.key.get_pressed()
    def collide_with_platforms(self):                     
          hits = pg.sprite.spritecollide(self, self.game.platforms, False)
          if hits:  
            if hits[0].is_slippery:                       
                        if self.vel.x>0:
                           self.vel.x+=0.5
                        elif self.vel.x<0:
                            self.vel.x-=0.5  
            if self.vel.y > 0 and self.pos.y<hits[0].rect.top:
             self.pos.y = hits[0].rect.top - self.rect.height             
             self.vel.y = 0
            self.rect.y = self.pos.y
                        
    def climbing(self):
       if self.can_climb:
        PLAYER_GRAV=0
        self.vel.y-=1
    def near_ladder(self):
        hits=pg.sprite.spritecollide(self,self.game.ladders,False)
        if hits:
            self.can_climb=True
        else:
            self.can_climb=False
            
    def first_initialization(self):
        while True:
            b=input("Enter your name: ")

            self.nick_name=b.strip()
            if len(self.nick_name)<20:
                break
            else:
                print("Please enter correct name")
        print(get_text('class'))
        a=input(get_text('read more')).lower()
        if a=='y' or a=='yes' or a=='yeah' or a=='ok' or a=='ага' or a=='yep':
           
           print(get_text('initialization'))
        a=input(get_text("class_choose")).strip()
        

        if   a=='warrior' or a.startswith('1'):
            self.spec='warrior'
          

        elif  a=='wizard' or a.startswith('2'):
            self.spec='wizard'
           
        elif  a=='archer' or a.startswith('3'):
            self.spec='archer'
           
        elif   a=='priest' or a.startswith('4'):
            self.spec='priest'
            
        else:
            print(get_text('wrong'))

        print(get_text('confirm')+self.spec)
    def collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == 'y':
            
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    if hits[0].is_slippery:
                       
                        if self.vel.x>0:
                           self.vel.x+=0.5
                        elif self.vel.x<0:
                            self.vel.x-=0.5
                                 

                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                    
                self.vel.y = 0
                self.rect.y = self.pos.y
                    
        
        
  
    def jump(self):
            
            self.rect.y+=1
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                
                self.vel.y-=16           
            self.rect.y-=1

            self.rect.y+=1
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                
                self.vel.y-=16           
            self.rect.y-=1

    
    def update(self):
        self.get_keys()
        self.acc = vec(0, GRAVITY)
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC    

       

        self.acc.x += self.vel.x * PLAYER_FRICTION      
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc      
        self.rect.x = self.pos.x
        self.collide('x')
        self.rect.y = self.pos.y
        self.collide('y')
        

       



    

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h,is_slippery=False):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.x=x
        self.y=y
        self.is_slippery=is_slippery
        self.rect.x=x
        self.rect.y=y
       


class Enemy(pg.sprite.Sprite):
    def __init__(self,game,x,y,type,level):
       

        #базовое
        self.groups=game.enemies,game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.rot='right'
        self.image=pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(LIGHTGREY)
        self.game=game
        
        self.type=type
       
        if self.type=='primitive':
            self.id=0
        elif self.type=='passive':
            self.id=1
        elif self.type=='ninja':
            self.id=2
            
        elif self.type=='jumper':
            self.id=3
        elif self.type=='canon':
            self.id=4
            self.image=pg.image.load(canon_image)
        elif self.type=='star':
            self.id=5
        self.image.set_colorkey(WHITE)
        self.left_image=pg.transform.flip(self.image,True,False)
        self.right_image=self.image
        
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.vel=vec(0,0)
        self.pos=vec(x,y)
        self.acc = vec(0, 0)
        self.state='right'
        self.rot=vec(1,0)
        with open(enemies_file) as file:
            self.data=json.load(file)
        self.basic=self.data[self.id]
        #характеристика моба
        

        self.level=level
        self.range=self.basic['range']
        self.agro_radius=self.basic['agro_radius']
        self.type=self.basic['type']
        self.speed=self.basic['speed']
        self.exp=self.basic['exp']
         #прирост
        self.inc_p_armor=self.basic['inc_p_armor']
        self.inc_m_armor=self.basic['inc_m_armor']
        self.inc_health=self.basic['inc_health']
        #Здоровье
        self.max_health=self.basic['Basic health']+self.level*self.inc_health
        self.health=self.max_health
        #Броня
        self.p_armor=self.basic["Basic p_armor"]+self.level*self.inc_p_armor
        self.m_armor=self.basic["Basic m_armor"]+self.level*self.inc_m_armor
        #атака
        self.damage=int(self.basic['damage']+self.level*self.basic["mod"])
        self.type_of_damage=self.basic['type_of_damage']
        self.last_attack=pg.time.get_ticks()
        self.attack_speed=self.basic["attack speed"]*1000
        self.exp=self.exp*self.level

        #логи
        self.creation_time=pg.time.get_ticks()
        self.list_of_attacks=[]
       


    def jump(self):
            self.rect.y+=1
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vel.y-=16
            self.rect.y-=1
    def collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
    def draw_health_bar(self):

       if self.health > 0.6*self.max_health:

            col = GREEN

       elif self.health > 0.3*self.max_health      :

            col = YELLOW

       else:

            col = RED

       width = int(self.rect.width * (self.health / self.max_health))

       self.health_bar = pg.Rect(0, 0, self.rect.width, 7)

       if self.health < self.max_health:

            pg.draw.rect(self.image, col, self.health_bar)

    def detect_enemy(self):
        self.detected=[]
        for hero in self.game.heroes:
            if math.fabs(hero.pos.x-self.pos.x)<self.agro_radius:
           
                if math.fabs(hero.pos.y-self.pos.y)<self.agro_radius:
                    self.detected.append(hero)
                    return True

    def can_attack(self):
        for hero in self.game.heroes:
            if math.fabs(hero.pos.x-self.pos.x)<self.rect.width*1.1:
                if math.fabs(hero.pos.y-self.pos.y)<self.rect.height*1.1:
                    return True
    def attack_enemy(self):
        now = pg.time.get_ticks()
        if now - self.last_attack >= self.attack_speed:
                    self.last_attack = now  
                    if self.state=='right':
                        self.list_of_attacks.append(Attack(self.game,vec(self.pos.x,self.pos.y),vec(1,0),self.damage,self.type_of_damage,'punch','heroes',w=self.rect.width,h=self.rect.height))
                        
                    elif self.state=='left':
                        self.list_of_attacks.append( Attack(self.game,self.pos,vec(self.pos.x,self.pos.y),self.damage,self.type_of_damage,'punch','heroes',w=self.rect.width,h=self.rect.height))
                     
                      
    def can_attack_range(self):
        self.detected=[]
        for hero in self.game.heroes:
            if math.fabs(hero.pos.x-self.pos.x)<self.agro_radius:
           
                if math.fabs(hero.pos.y-self.pos.y)<self.agro_radius:
                    self.detected.append(hero)
                    return True


    def dodge_range(self):
       for bullet in self.game.attacks:
           if bullet.type_of_attack!='meteor' and bullet.type_of_attack!='punch':
               if bullet.danger=='enemies':
                   if abs(bullet.pos.x-self.pos.x)<=self.rect.width*5:
                       if bullet.pos.y <=self.rect.bottom and bullet.pos.y>=self.rect.top:
                           
                           self.jump()
    def dodge_melee(self,chance):            #шанс увернутся в процентах
          for bullet in self.game.attacks:
              if bullet.type_of_attack=='punch':
                  if bullet.danger=='enemies' or bullet.danger=='all':
                      i=random.randint(1,100)
                      image=self.image
                      if i<chance:
                        if abs(bullet.pos.x-self.pos.x)<=self.rect.width*2:
                         if bullet.pos.y <=self.rect.bottom and bullet.pos.y>=self.rect.top:  
                           if self.rot=='right':
                               self.vel.x+=100
                           else:
                                self.vel.x-=100
                           
                          
                             

                           
    def move(self,dir):
        if dir=='right':
            self.acc.x = -PLAYER_ACC*self.speed
            self.rot='right'
           
        elif dir=='left':
            
            self.acc.x = PLAYER_ACC*self.speed
            self.rot='left'
    def move_to_enemy(self):
        for enemy in self.detected:
            if enemy.pos.x-self.pos.x>0: #cлева
                self.move('left')
                self.state='left'
            
            else:
                self.move("right")
                self.state='right'
    def following_jump(self):
        if self.vel.y==0 and self.vel.x==0:
            
                        self.jump()
        for enemy in self.detected:
            if enemy.jumping==True:
                self.jump()
    def random_jumping(self):
            self.jump()
    def canon_shoot(self):
         for enemy in self.detected:
            if enemy.pos.x-self.pos.x>0: #cлева
               
                    self.state='right'
            else:
                self.state='left'
         now = pg.time.get_ticks()
         if now - self.last_attack >= self.attack_speed:
                    self.last_attack = now
                    for detected in self.detected:
                     self.list_of_attacks.append(Attack(self.game,vec(self.rect.centerx,self.rect.centery),vec(self.rect.centerx-detected.rect.centerx,self.rect.centery-detected.rect.centery).normalize(),self.damage,self.type_of_damage,'canon_ball','heroes'))
                     
                     
 
    def star_shoot(self):
          speed=10
          now = pg.time.get_ticks()
          if now - self.last_attack >= self.attack_speed:
                    self.last_attack = now
                    
                    Attack(self.game,vec(self.pos.x,self.pos.y),vec(-1,0),self.damage,self.type_of_damage,'mini_missle','heroes')
                    Attack(self.game,vec(self.pos.x,self.pos.y),vec(1,0),self.damage,self.type_of_damage,'mini_missle','heroes')
                    Attack(self.game,vec(self.pos.x,self.pos.y),vec(0,-1),self.damage,self.type_of_damage,'mini_missle','heroes')
                    Attack(self.game,vec(self.pos.x,self.pos.y),vec(0,1),self.damage,self.type_of_damage,'mini_missle','heroes')
    def ninja_AI(self):
         if self.detect_enemy():
                if self.can_attack():
                 self.attack_enemy()
                 
                 self.dodge_melee(20)
                if self.can_attack()!=True:
                    self.move_to_enemy()
                    
                    self.following_jump()
         else:
               self.dodge_range()
    def canon_AI(self):
        if self.detect_enemy():
            if self.can_attack_range():
                self.canon_shoot()
    def star_AI(self):
        if self.detect_enemy():
             self.star_shoot()
            
    def primitive_AI(self):
        if self.detect_enemy():
                if self.can_attack():
                 self.attack_enemy()
                if self.can_attack()!=True:
                    self.move_to_enemy()              
        else:
               pass
    def passive_AI(self):      
           if self.detect_enemy():
                if self.can_attack():
                 self.attack_enemy()
                if self.can_attack()!=True:
                    self.move_to_enemy()              
           else:
              self.dodge_range()
    def jumper_AI(self):
        if self.detect_enemy():
                if self.can_attack():
                 self.attack_enemy()
                if self.can_attack()!=True:
                    self.move_to_enemy()       
                    self.random_jumping()
        else:
              pass
    def AI(self):
        if self.type=='primitive':
            self.primitive_AI()
        elif self.type=='passive':
            self.passive_AI()
        elif self.type=='ninja':
            self.ninja_AI()
        elif self.type=='jumper':
            self.jumper_AI()
        elif self.type=='canon':
            self.canon_AI()
        elif self.type=='star':
            self.star_AI()
             
    def necrologue(self):
        if self.health>0:
            live=True
        else:
            live=False
        dealed_damage=0
        accuracy=0
        hits=0
        i=0
        lasthit=False    
        for attack in self.list_of_attacks:
            i+=1
            try:
                if attack.attacked:
                    dealed_damage+=attack.total_damage                 
                    hits+=1
            except:
                pass
            try:
                lasthit=attack.lasthit
            except:
                pass
        try:
           accuracy=round((hits/i),2)
        except:
            accuracy=0
        

        dictionary={"type":self.type,"level":self.level,"time survived":int((pg.time.get_ticks()-self.creation_time)/1000),
                        "dealed damage":dealed_damage,"accuracy":accuracy,"last hit":lasthit,"survived":live}
        self.game.necrologue_list.append(dictionary)
       
      
    def update(self):
        if self.speed!=0:
            self.acc = vec(0, GRAVITY)
        if self.state=="right":
            self.image=self.right_image
        else:
            self.image=self.left_image
        self.AI()
        self.acc.x += self.vel.x * PLAYER_FRICTION      
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc         
        self.rect.x = self.pos.x
        self.collide('x')
        self.rect.y = self.pos.y
        self.collide('y')
        self.draw_health_bar()
       
        if self.health<=0:
          
          self.necrologue()
          self.kill()
          
         
          for hero in self.game.heroes:
              if self.exp>0:

                  
                  delta=hero.level-self.level
                  exp=int(self.exp/len(self.game.heroes))
                  hero.exp+=exp+1
                  self.exp-=exp+1
                  Floating_number(self.game,self.pos.x,self.pos.y,"+"+str(exp)+" exp","expirence")
             
              
        
class Actor(pg.sprite.Sprite):
    def __init__(self,game,x,y,plot_name,sub_stat=0):
        self.game=game
        
        self.groups=game.all_sprites,game.actors
      
        pg.sprite.Sprite.__init__(self,self.groups)
        self.state='right'
        self.start=vec(x,y)
        self.plot="plot_"+plot_name+".py"
        self.image=pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(BLACK)
        self.game=game
        self.type=type
        self.active=False
        self.spawn_time=pg.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
        self.vel=vec(0,0)
        self.pos=vec(x,y)
        self.acc = vec(0, 0)
        self.detect_trigger=1
        self.load_trigger=1
        self.execute_trigger=1
        self.condition="staying"
        self.begin_time=pg.time.get_ticks()
        self.shoot_rot=vec(-1,0)  
        
      

        

        self.load_plot()
        spec = importlib.util.spec_from_file_location(self.plot, PLOT_FOLDER+self.plot)
        plot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plot)
        self.activation_radius=plot.radius
        self.living_time=plot.life_time
        self.call_key=plot.call_key
        try:
           self.shots=plot.shots
        except:
            pass
        self.name=plot.name
        self.icon=pg.image.load(plot.icon_path)
        try:
           self.initiator=plot.initiator
        except:
            self.initiator=False
        self.image=self.icon
        self.timer=5000
        self.est_timer=pg.time.get_ticks()
    def load_plot(self):

       
       
        spec = importlib.util.spec_from_file_location(self.plot, PLOT_FOLDER+self.plot)
        plot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plot)
        
        
    def show_words_on_second(self,string,timer,time_pos,begin_time):
        now=pg.time.get_ticks()
  
        if pg.time.get_ticks()>=begin_time+time_pos*1000 and pg.time.get_ticks()<=begin_time+timer*1000+time_pos*1000:
         Floating_number(self.game,self.game.player_1.pos.x-100,self.game.player_1.pos.y+400,string,"words",timer)
         Floating_number(self.game,self.game.player_1.pos.x-420,self.game.player_1.pos.y+470,self.name,"words",timer)
         HUD.draw_player_icon(self.game.screen,self.icon,vec(0,0))
        
              
    

    def activate(self):
        if self.detect_trigger>0:
            for hero in self.game.heroes:
                if math.fabs(hero.pos.x-self.pos.x)<self.activation_radius:
            
                    if math.fabs(hero.pos.y-self.pos.y)<self.activation_radius:
                        self.activation_time=pg.time.get_ticks()
                        self.active=True
                        self.load_trigger-=1
                        self.detect_trigger-=1
                       
    def call(self,trigger):
        for actor in self.game.actors:
            if actor.call_key==trigger:
                actor.active=True         
                actor.load_trigger-=1
                actor.detect_trigger-=1

    def die_after_ending(self):
        try:
            now=pg.time.get_ticks()
            if now - self.activation_time>=self.living_time*1000:
                
               
                self.kill()
                
        except:
            pass
    def bug_fix_1(self):
        if pg.time.get_ticks()-self.spawn_time-7000<=self.timer:
           
            self.pos=self.start
    def collide(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
        
        if self.vel.y==0:
            self.state='standing'
    def move(self,dir,speed):
        if dir=='right':
            self.vel.x=speed
           
           
            self.rot='right'
           
            self.shoot_rot=vec(-1,0)    
        elif dir=='left':
            self.vel.x=-speed
            self.rot='left'
            self.shoot_rot=vec(1,0)    
        elif dir=='up':
            self.vel.y=-speed*self.dir.x
            
        elif dir=='down':
            self.vel.y=-speed*self.dir.x
            

    def update(self):
        self.bug_fix_1()
        self.die_after_ending()
        self.activate()
        for hero in self.game.heroes:
                if math.fabs(hero.pos.x-self.pos.x)<self.activation_radius:
           
                    if math.fabs(hero.pos.y-self.pos.y)<self.activation_radius:
                        hero.cutscene_down.active=True
                        hero.isScene=True
       
        if self.load_trigger!=1 and self.execute_trigger==1:         
            self.condition="acting"
            self.execute_trigger-=1
         
            self.begin_time=pg.time.get_ticks()
  
           
        if self.condition=="acting":
             spec = importlib.util.spec_from_file_location(self.plot, PLOT_FOLDER+self.plot)
             plot = importlib.util.module_from_spec(spec)
             spec.loader.exec_module(plot)    
             
             plot.execute(self,self.begin_time)
        
      
        self.acc = vec(0, GRAVITY)
        self.acc.x += self.vel.x * PLAYER_FRICTION    
        
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc 
        
         
       
        self.rect.x = self.pos.x
        self.collide('x')
        self.rect.y = self.pos.y
        self.collide('y')
        


class Item(pg.sprite.Sprite):
     def __init__(self, game, x, y,id,iscode=False,is_hidden=False,rand_rarity=None):      #пока что id это номер в списке (зашифровать)
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game=game
        
        self.iscode=iscode
     
        if is_hidden:
             self.image = pg.Surface([TILESIZE,TILESIZE], pg.SRCALPHA,32)
        else:

            self.image = pg.Surface((TILESIZE, TILESIZE))                     #ТЕСТОВАЯ ТЕКСТУРА (ИЗМЕНИТЬ!)
            self.image.fill(RED)
        self.id=id
        self.rect = self.image.get_rect()
        self.pos=vec(x,y)
       
       
        with open(items_file) as file:
             file_data=json.load(file)
        if rand_rarity!=None:
            self.rarity=rand_rarity
            while True:
                self.id=random.randint(0,len(file_data)-1)
                self.basic=file_data[self.id]
                if self.basic['rarity']==self.rarity:                 
                    break
                   
        
        
        #присваивание атрибутов
        self.basic=file_data[self.id]
        self.name=self.basic['name']
        self.rarity=self.basic['rarity']
        self.level=self.basic['level']
        self.mod=self.basic['mod']
        self.type=self.basic['type']
        if self.type=='grenade':
            self.damage=self.level*self.mod
            self.type_of_damage=self.basic['type_of_damage']
        if self.type=='armor' or self.type=='weapon':  #ибо броня и оружие одеваются на часть тела
         self.part=self.basic['part of body']
         
        if self.type=='potion':
            self.action=self.basic['action']
        self.set_mods()

     def set_mods(self):               #редкость предмета пока линейная (возможно изменение)
         if self.rarity=='usual':
             self.rar_mod=1
         elif self.rarity=='rare':
             self.rar_mod=2
         elif self.rarity=='unique':
             self.rar_mod=3
         elif self.rarity=='legendary':
             self.rar_mod=4
         elif self.rarity=='epic':
             self.rar_mod=5

         if self.type=='armor':
             
             self.weight=self.basic['weight']         #чем "тяжелее" броня тем она лучше защищает (возможно изменение)
             if self.weight=='cloth':
                 self.weight_int=0
             elif self.weight=='light':
                 self.weight_int=1
             elif self.weight=='medium':
                 self.weight_int=2
             elif self.weight=='heavy':
                 self.weight_int=3
             elif self.weight=='superheavy':
                 self.weight_int=4
             self.armor=self.level*self.rar_mod+self.mod*self.weight_int #уровень на редкость плюс модификатор на вес (возможно изменение)
         elif self.type=='weapon':
             self.damage=self.level*self.rar_mod+self.mod
         try:
           if self.type=='potion':
              if self.action=='health'or self.action=='mana':
                self.restoring=self.level*self.rar_mod*self.mod
         except:
             pass
         try: 
           self.usable_as_under=self.basic['usable_as_under']
         except KeyError:
             self.usable=False
         try: 
           self.iscursed=self.basic['iscursed']
         except KeyError:
            self.iscursed=False
         try:
            if self.type=='armor':
                if self.basic['Protection from magic']:
                    self.magic_protection=round(self.armor/2)
         except KeyError:
             self.magic_protection=0

         try: 
           self.isHoly=self.basic['isHoly']
           
         except KeyError:
             self.isHoly=False
     def pick_up(self):
           hits=pg.sprite.spritecollide(self,self.game.heroes,False,False)
           if hits:        
            for hit in hits:
                
                    Floating_number(self.game,hit.pos.x,hit.pos.y-300,"Collected "+self.name,"words")
                    HUD.show_information_log(self)               
                    if len(hit.inventory)<hit.inventory_capacity:
                         hit.inventory.append(self)
             
                         self.kill()
                    else:  
                       Floating_number(self.game,hit.pos.x,hit.pos.y,"Your inventory is full.","words")


     def update(self):
        if not self.iscode:
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            self.pick_up()
        else:
             self.kill()
  






class Attack(pg.sprite.Sprite):
    def __init__(self,game,startpos,direction,damage=0,type_of_damage='physical',type_of_attack='punch',danger='all',isSimple=True,w=64,h=64,isStunning=False):
        self.groups=game.attacks,game.all_sprites
        
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.start_w=w
        self.start_h=h
        self.pos=startpos
        self.dir=direction
        self.simple=isSimple
        self.damage=damage
        self.type_of_damage=type_of_damage
        self.isStunning=isStunning
        self.type_of_attack=type_of_attack
        self.danger=danger
        
        self.speed_constant=20

        self.size()
        self.set_image()
        self.rect=self.image.get_rect()
        


        self.creation = pg.time.get_ticks()
        
       


       


        self.vel=vec(0,0)
       
        self.acc=vec(0,0)
       
   
        

    
    def death_timer(self):
        if pg.time.get_ticks() - self.creation >= self.death_time:
            self.kill()
    def set_image(self):
        
        if self.type_of_attack=='punch':
           self.image = pg.Surface([self.width,self.height], pg.SRCALPHA,32)
               

        elif self.type_of_attack=='arrow':
         self.image=pg.Surface([self.width,self.height])
         self.image.fill(GREEN)
            
        elif self.type_of_attack=='magic_missle':
         self.image=pg.Surface([self.width,self.height])
         self.image.fill(GREEN)
        elif self.type_of_attack=='bullet':
         self.image=pg.Surface(self.width,self.height)
         self.image.fill(GREEN)
       
           
        elif self.type_of_attack=='grenade':
         self.image=pg.Surface([self.width,self.height])
         self.image.fill(GREEN)
            
        elif self.type_of_attack=='canon_ball':
         self.image=pg.Surface([self.width,self.height])
         self.image.fill(GREEN)
        elif self.type_of_attack=='mini_missle':
         self.image=pg.Surface([self.width,self.height])
         self.image.fill(GREEN)
        elif self.type_of_attack=='meteor':
         self.image=pg.Surface([self.width,self.height])
         self.image.fill(GREEN)
       
    
    def size(self):
        if self.type_of_attack=='punch':
            
            speed_k=0
            width=1.2*self.start_w
            height=self.start_h
            self.death_time=30
            distance='melee'
            self.penetration=True
            self.dir=self.dir.reflect(vec(1,0))
            
            if self.dir.x>=-1.01 and self.dir.x<=0.99:
                self.pos.x-=self.start_w
                

        elif self.type_of_attack=='arrow':
            speed_k=1
            width=50
            height=10
            self.death_time=5000
            distance='ranged'
            
        elif self.type_of_attack=='magic_missle':
            speed_k=0.75
            width=20
            height=15
            self.death_time=4000
            distance='ranged'
        elif self.type_of_attack=='bullet':
            
            speed_k=1.5
            width=10
            height=10
            self.death_time=3000
            distance='ranged'
        elif self.type_of_attack=='grenade':
            
            speed_k=0.125
            width=15
            height=15
            self.death_time=4000
            distance='ranged'
            self.is_falling=True
        elif self.type_of_attack=='canon_ball':
            self.gravity=True
            width=30
            height=30
            self.death_time=6000
            speed_k=0.5
            distance='ranged'
        elif self.type_of_attack=='mini_missle':
            
            width=5
            height=5
            self.death_time=2000
            speed_k=1.2
            distance='ranged'
        elif self.type_of_attack=='meteor':
            width=32
            height=32
            self.death_time=1000
            speed_k=1
            distance='ranged'
            self.penetration=True
        try:
            if self.penetration==True:
                self.penetration=True
        except:
            self.penetration=False
        try:
            if self.is_falling==True:
                self.is_falling=True
        except:
            self.is_falling=False
        self.width=width
        self.height=height
        self.speed=speed_k*self.speed_constant
        self.distance=distance

    def start_timer(self):
        if pg.time.get_ticks()-self.creation>=300:
            return True
        else:
            return False

    def move(self):
        if self.distance!='melee':
            self.vel.x=-self.speed*self.dir.x
            self.vel.y=-self.speed*self.dir.y
         

    def gravity(self):
       self.acc=vec(0,GRAVITY/2)
    def collide_with_wall(self):
        
        if self.penetration==False:
         if self.start_timer():
             hits= pg.sprite.groupcollide(self.game.attacks,self.game.walls,True,False) 
             if hits:
                 self.collided=True
                
          
   
    def strike(self,group):
        hits=pg.sprite.spritecollide(self,group,False,False)
        if hits:
                for hit in hits:
                   
                     
                      if self.type_of_damage=='physical':
                        if self.damage-hit.p_armor<=0:
                          damage=1
                        else:
                         damage=self.damage-hit.p_armor
                      elif self.type_of_damage=='magical':
                        if self.damage-hit.m_armor<=0:
                          damage=1
                        else:
                         damage=self.damage-hit.m_armor
                      elif self.type_of_damage=='clear':
                        damage=self.damage
                       
                      hit.health-=damage
                      if self.isStunning:
                          hit.isStunned=True
                      Floating_number(self.game,hit.pos.x,hit.pos.y,"-"+str(damage),self.type_of_damage)
                      self.attacked=True
                      self.total_damage=damage
                      if hit.health<=0:
                          self.lasthit=True
                      self.kill()
                      
    def update(self):

       
      
       if self.is_falling:
        self.gravity()
       if self.danger=='heroes' or self.danger=='all':
         self.strike(self.game.heroes)
       
       if self.danger=='enemies' or self.danger=='all':
         self.strike(self.game.enemies)
         
       self.move()
       self.death_timer()
       
       
       self.vel += self.acc
       self.pos += self.vel + 0.5 * self.acc
       self.rect.x=self.pos.x
       self.rect.y=self.pos.y
       self.collide_with_wall()

class Trap(pg.sprite.Sprite):
    def __init__(self,game,x,y,w,h,type):
        self.groups=game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image= pg.Surface([w,h], pg.SRCALPHA,32)
        self.game=game
        self.rot=0
        self.rot_speed=60
        self.last_attack=pg.time.get_ticks()
        self.type=type
        self.frame=0
      
        self.last_animation=pg.time.get_ticks()
        if type=='usual':
            self.damage=20
            self.reload=1
            self.type_of_damage="physical"
        if type=="saw":
            self.damage=15
            self.image=pg.image.load(saw_image)
            self.image.set_colorkey(BLACK)
            self.orig=self.image
            self.reload=2
            self.type_of_damage="clear"

        self.x=x
        self.y=y
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    
    def attack_trap(self,group):
         hits=pg.sprite.spritecollide(self,group,False,False)
         
         if hits:
             for hit in hits:
                       if self.damage-hit.p_armor<=0:
                                   damage=1
                       else:
                                    damage=self.damage-hit.p_armor
                       #self.game.DJ.play_effect('slash')
                       hit.health-=damage
                       Floating_number(self.game,hit.pos.x,hit.pos.y,"-"+str(damage)+"hp",self.type_of_damage)

                   
                       self.last_attack=pg.time.get_ticks()
    def attack_saw(self,group):
         hits=pg.sprite.spritecollide(self,group,False,False)
         
         if hits:
             for hit in hits:
                   if pg.sprite.collide_mask(self,hit):             
                       damage=self.damage
                     #  self.game.DJ.play_effect('slash')
                       hit.health-=damage
                       Floating_number(self.game,hit.pos.x,hit.pos.y,"-"+str(damage)+"hp",self.type_of_damage)
                       self.last_attack=pg.time.get_ticks()
              

                      
 
        
           
       
    def update(self):
       
       if self.type=='saw':
           if pg.time.get_ticks()-self.last_attack>=self.reload*1000:
          
             self.attack_saw(self.game.enemies)
             self.attack_saw(self.game.heroes)
             self.rect.centerx=self.x
             self.rect.centery=self.y
           self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
           self.image = pg.transform.rotate(self.orig,self.rot)

       else:
          
          if pg.time.get_ticks()-self.last_attack>=self.reload*1000:
             self.attack_trap(self.game.heroes)
             self.attack_trap(self.game.enemies)
     
   




class Ladder(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self.groups = game.ladders
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.x=x
        self.y=y
        self.rect.x=x
        self.rect.y=y
class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h,rarity):
        
        self.groups = game.chests,game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.pos=vec(x,y)
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
        self.rarity=rarity
        self.num_of_items=6
        self.image = pg.Surface([w,h], pg.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.items=[]
        self.fill_with_items()
        
    def rand_item(self,type):
        while True:
            with open(items_file) as file:
                        data=json.load(file)
            i=random.randint(0,len(data)-1)
            item=Item(self.game,self.rect.x,self.rect.y,i)
            item.kill()
            if item.rarity==type:
                break
        return item
   
    def rand_selected(self,rarity,part):
        while True:
            with open(items_file) as file:
                        data=json.load(file)
            i=random.randint(0,len(data)-1)
            item=Item(self.game,self.rect.x,self.rect.y,i)
            item.kill()
            if item.rarity==rarity and item.type==part:
                break
            
        return item
   

    def use(self):
             print("This is "+self.rarity.upper()+" chest!")
             if len(self.items)>0:
                 safe=[]
                 print("It contains:")
                 i=1
                 
                 for item in self.items:
                     
                     print(str(i)+") "+item.name)
                     
                     i+=1
                     safe.append(item)
                 a=input("What you want to do? 1)take one item 2)take all 3)close ")
                 try:
                     if a.strip()=='1':
                         if len(self.game.player_1.inventory)<self.game.player_1.inventory_capacity:
                            choosen_item=safe[int(input("What item you want to take? "))-1]
                            self.items.remove(choosen_item)
                            HUD.show_information(choosen_item)
                            self.game.player_1.inventory.append(choosen_item)
                         else:
                            print(get_text("full"))
                     if a.strip()=='2':
                         if len(self.game.player_1.inventory)+5<self.game.player_1.inventory_capacity:
                           self.game.player_1.inventory.extend(self.items)
                           for item in self.items:
                               HUD.show_information(item)
                           self.items=[]
                           
                         else:
                             print(get_text("full"))
                       

                     if a.strip()=='3':
                         print("Confirmed.")
                 except:
                     pass

             else:
                 print("And this chest is empty!")
               
           
    def fill_with_items(self):
        
        if self.rarity=='usual':             
         self.items.append(self.rand_item('usual'))
         self.items.append(self.rand_item('usual'))  
         self.items.append(self.rand_item('usual'))  
         self.items.append(self.rand_selected('usual','potion'))
         self.items.append(self.rand_selected('usual','weapon'))

        elif self.rarity=='rare':
           
           self.items.append(self.rand_selected('rare','weapon'))
           self.items.append(self.rand_selected('usual','potion'))
           self.items.append(self.rand_selected('usual','armor'))
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('usual'))
        elif self.rarity=='unique':
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('rare'))
           self.items.append(self.rand_item('unique'))
        elif self.rarity=='legendary':
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('rare'))
           self.items.append(self.rand_item('unique'))
           self.items.append(self.rand_item('legendary'))
        elif self.rarity=='epic':
           self.items.append(self.rand_item('usual'))
           self.items.append(self.rand_item('rare'))
           self.items.append(self.rand_item('unique'))
           self.items.append(self.rand_item('legendary'))
           self.items.append(self.rand_item('epic'))
    def update(self):
      self.rect.x=self.pos.x
      self.rect.y=self.pos.y


class Hint(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h,name):
        self.groups = game.hints,game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name=name
        if self.name.endswith("music"):
            self.type="music_trigger"
        else:
            self.type="hint"
        if self.type=="music_trigger":
            list=self.name.split("_")
            self.music=list[2]
            
        elif self.type=="hint":
            self.id=self.name[-2:]
        self.rect=pg.Rect(x,y,w,h)
        self.pos=vec(x,y)
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
      
        self.image = pg.Surface([w,h], pg.SRCALPHA,32)
        self.image = self.image.convert_alpha()
    def hitting(self):
        if pg.sprite.spritecollide(self,self.game.heroes,False,False):
            self.activate()
            self.kill()
    def activate(self):
        if self.type=="hint":
            with open(languages_folder+language_manager.get_language()+"\\hint_"+self.id+".txt") as file:
                line=file.read()
                print(line)
        elif self.type=="music_trigger":
             self.game.DJ.play_music(self.music)
             self.kill()
            
    def update(self):
      self.hitting()
      self.rect.x=self.pos.x
      self.rect.y=self.pos.y





class Stick(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h):
        self.groups = game.sticks,game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,w,h)
        self.pos=vec(x,y)
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
        self.id=num_of_hint
        self.image = pg.Surface([w,h], pg.SRCALPHA,32)
        self.image = self.image.convert_alpha()
    def is_onground(self):
        if pg.sprite.spritecollide(self,self.game.walls,False):
            return True
        else:
            False
    

  


class Floating_number(pg.sprite.Sprite):
    def __init__(self, game, x, y,string,type,timer=2):
        self.groups = game.text,game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.string=string
        self.font=READABLE_FONT

        self.death_timer=1200
        self.pos=vec(x,y-TILESIZE*1.5)
        self.speed=0.5
        self.color=BLACK
        if self.string.isdigit():
            self.get_text(self.string)
        if type=="physical":
            self.color=RED
        elif type=='magical':
            self.color=(0,0,255)
        elif type=='clear':
            self.color=WHITE
        elif type=='expirence':
            self.color=YELLOW
        elif type=='mana':
             self.color=(55,86,186)
             self.pos=vec(x-TILESIZE*1.5,y-TILESIZE*1.5)
        elif type=='sign':
             self.color=WHITE
             self.death_timer=1500
        elif type=='log':
             self.color==LIGHTGREY
             
        elif type=='words':
            self.color=WHITE
            self.death_timer=timer*1000
            self.speed=0
            
            self.death_timer=2000
        elif type=="permanent words":
            self.pos=vec(x,y)
            self.speed=0
            self.color=WHITE
            self.death_timer=None
        elif type=="commentary":
            self.color=WHITE
            self.pos=vec(WIDTH/3,(HEIGHT/3)*2)
            self.speed=0
            self.death_timer=30000
        elif type=="GLOBAl":
            self.color=(140,18,0)
            self.pos=vec(WIDTH/3,(HEIGHT/3)*2)
            self.speed=0
            self.death_timer=4
        self.image=self.draw_numbers(self.string,self.font,28,self.color,self.pos.x,self.pos.y)
        self.rect=self.image.get_rect()
       
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
      
        
        
        
        self.last=pg.time.get_ticks()
    def set_timer(self,seconds):
        self.death_timer=seconds*1000
    def draw_numbers(self, text, font_name, size, color, x, y, align="nw"):     
        font = pg.font.Font(font_name, size)

        text_surface = font.render(text, False, color)

        text_rect = text_surface.get_rect()

        if align == "nw":

            text_rect.topleft = (x, y)

        if align == "ne":

            text_rect.topright = (x, y)

        if align == "sw":

            text_rect.bottomleft = (x, y)

        if align == "se":

            text_rect.bottomright = (x, y)

        if align == "n":

            text_rect.midtop = (x, y)

        if align == "s":

            text_rect.midbottom = (x, y)

        if align == "e":

            text_rect.midright = (x, y)

        if align == "w":

            text_rect.midleft = (x, y)

        if align == "center":

            text_rect.center = (x, y)

        return text_surface
    
    def float_up(self):
         self.pos.y-=self.speed
    def die(self):
        if self.death_timer!=None:
            now = pg.time.get_ticks()
            if now - self.last >= self.death_timer:
                self.kill()
               # for hero in self.game.heroes:
                   # hero.cutscene_up.clear()
                  #  hero.cutscene_down.clear()
    def get_text(self,name):
        with open(languages_folder+language_manager.get_language()+"\\words_"+name+".txt") as file:
         self.string=file.read()
    def update(self):
      
      self.float_up()
      self.die()
      self.rect.x=self.pos.x
      self.rect.y=self.pos.y


class SpriteList:

   

    def __init__(self, filename):

        self.spritelist = pg.image.load(filename).convert()



    def get_image(self, x, y, width, height):

       

        image = pg.Surface((width, height))

        image.blit(self.spritelist, (0, 0), (x, y, width, height))

        

        return image




class Spawn(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.spawns,
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect=pg.Rect(x,y,1,1)
        self.pos=vec(x,y)
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
        self.it=0
        self.image = pg.Surface([1,1], pg.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.last_spawn=pg.time.get_ticks()
        self.to_load=[]
        
    def load_global_pack(self,pack):
      
        self.global_pack=pack
    def load_local_pack(self):
        self.to_load=[]
        for enemy in self.global_pack:
            
            self.to_load.append({"type":enemy["type"],"level":enemy["level"],"amount":(enemy["amount"]/len(self.game.spawns))})


    def spawn(self):
        for enemy in self.to_load:
            while enemy["amount"]>0:
                enemy["amount"]-=1
                spread=random.randint(-20,20)
                pos=vec(self.pos.x+spread,self.pos.y)
                type=enemy["type"]
                level=enemy["level"]
                archive=[pos,type,level]
                self.game.player_1.spawn_enemy(archive)
        
    def spawn_after(self,seconds):
        if pg.time.get_ticks()-self.last_spawn>=seconds*1000:
            self.spawn()
            self.last_spawn=pg.time.get_ticks()
           
    def update(self):
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
        if self.it==0:
            self.spawn()
            
            self.it-=1
        self.spawn_after(5)
        

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y,w,h,is_slippery=False):
            self.groups = game.platforms
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.rect=pg.Rect(x,y,w,h)
            self.is_slippery=is_slippery
            self.rect.x=x
            self.rect.y=y

        

   
           
