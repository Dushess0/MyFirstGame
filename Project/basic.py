
import pygame as pg
import sprites
import threading
import _thread
import json
import time
import HUD
from settings import *
import random
import equation_manager
from language_manager import language_text as text
from sprites import give_named_item_code
vec=pg.math.Vector2

def question(a):
    a=a.lower()
    if a=='y' or a=='yes' or a=='yeah' or a=='ok' or a=='ага' or a=='yep' or a=='yes of course':
        return True
    else:
        return False





class Basic(sprites.Player):
    def __init__(self, game, start_x, start_y):
        super().__init__(game, start_x, start_y)
        
        self.state='right'
        self.multi()
        self.rot=vec(-1,0)
        self.angle=0
        self.isStunned=False
        self.life=True
        self.list_of_attacks=[]
        self.wave=0
        self.pos=vec(start_x,start_y)
        
        with open(basic_file) as file:
                data=json.load(file)
            
         
        try:
            with open(saving_file) as file:
                saving=json.load(file)
            self.load_data()
            
        except FileNotFoundError:
            #если первый запуск
            self.level=1
            self.first_initialization()
            self.load_images(data)
            self.orig=self.image
            self.rect = self.image.get_rect()
            self.intelligence=1
            self.strenght=1
            self.endurance=1
            self.agility=1
            self.spirit=1
            self.exp=0
            self.free_points=10
            self.refresh_atributes()
            self.charges_of_ultimate=0
            self.health=self.max_health
            self.mana=self.max_mana
            self.p_armor=self.basic["Basic p_armor"]
            self.m_armor=self.basic["Basic m_armor"]
            self.armor_type=self.basic['Armor type']
            self.spec=self.basic["Class Name"]
            self.type=self.basic["Type of equations"]
            if self.armor_type=='cloth':
                self.rank_of_armor=0
            elif self.armor_type=='light':
                self.rank_of_armor=1
            elif self.armor_type=='medium':
                self.rank_of_armor=2
            elif self.armor_type=='heavy':
                self.rank_of_armor=3
            elif self.armor_type=='superheavy':
                self.rank_of_armor=4
            
            
            self.inventory=[]
            self.give_start_equipment()
            self.equiped_items={'head':None,
                            'body':None,
                            'under armor':None,
                            'gloves':None,
                            'boots':None,
                            'greave':None,
                            'right hand':None,
                            'left hand':None, 
                            'both':None
                            }
            self.save_data()
            self.game.player_1=Basic(self.game,self.pos.x,self.pos.y)
       
        #прирост
        self.refresh_atributes()
        
        
        #востановление
        
        self.last_mana_rest = pg.time.get_ticks()
        self.last_health_rest=pg.time.get_ticks()

        self.try_to_restore=pg.time.get_ticks()
        
        self.restore_cooldown=1000
       
        #cкорость атаки 
        
        self.last_punch=pg.time.get_ticks()

        self.last_ability=pg.time.get_ticks()

        self.last_ultimate=pg.time.get_ticks()

        self.temp_clock=pg.time.get_ticks()

        self.try_to_solve=pg.time.get_ticks()
        self.pick_up_timer=1000
        self.trying_timer=3000
        self.last_pick_up=pg.time.get_ticks()
        self.inventory_capacity=20
        #инвертарь
        self.inv=HUD.Inventory_HUD(self.game,0,0,self)
        
        self.stats=HUD.Stats_HUD(self.game,0,0,self)
        self.ultimate_timer=pg.time.get_ticks()       


        self.cutscene_up=HUD.CutScene_part(self.game,vec(0,0),self)

        self.cutscene_down=HUD.CutScene_part(self.game,vec(0,0),self)
        
        self.refresh_weapon_damage()
        if self.spec=='warrior':
            self.active_manacost=5
            self.ultimate_manacost=10
        elif self.spec=='wizard':
            self.active_manacost=10
            self.ultimate_manacost=20
        elif self.spec=='archer':
            self.active_manacost=5
            self.ultimate_manacost=10
        elif self.spec=='priest':
            self.active_manacost=5
            self.ultimate_manacost=8

        #анимация 

        self.icon=self.icon=pg.image.load(ICON_FOLDER+self.spec+".png")

        self.isScene=False
        self.last_animation=0
        self.walking=False
        self.jumping=False
        self.falling=False
        self.frame=0
        self.attacking=False
       
        self.laying=pg.transform.rotate(self.image,90)
        self.load_animation()
       
        self.begin_attack=pg.time.get_ticks()


        #классы и пути
        self.set_path()
        
        self.charges_of_ultimate=0
    def set_path(self):
        strenght=["warrior","soldier","knight","barbarian"]
        intelligence=["wizard","pyromancer","electro wizard","lich"]
        agility=["archer","gunslinger","assasin","ranger"]
        spirit=["priest","monk","paladin","heretic"]
        paths={"strenght":strenght,"intelligence":intelligence,"agility":agility,"spirit":spirit}
        for key,value in paths.items():
            for type in value:
                if self.spec==type:
                    self.path=key
                    break

       
    
    def load_images(self,data):
        if self.spec=='warrior':
                self.basic=data[0]
                
                self.sprite_list=sprites.SpriteList(warrior_sprite_list)
                self.image=self.sprite_list.get_image(0,0,64,64)
                self.image.set_colorkey((255,255,255))
                self.color=LIGHTGREY          
                
        if self.spec=='wizard':
                self.basic=data[1]
                self.sprite_list=sprites.SpriteList(wizard_sprite_list)
                self.image=self.sprite_list.get_image(0,0,64,64)
                self.image.set_colorkey((255,255,255))
                self.color=(9,50,89)
                self.shoot_pos=10
        if self.spec=='archer':
                self.sprite_list=sprites.SpriteList(archer_sprite_list)
                self.image=self.sprite_list.get_image(0,0,64,64)
                self.image.set_colorkey((255,255,255))
                self.basic=data[2]
                self.color=(13,133,10)
                self.shoot_pos=10
        if self.spec=='priest':
                
                self.sprite_list=sprites.SpriteList(priest_sprite_list)
                self.image=self.sprite_list.get_image(0,0,64,64)
                self.image.set_colorkey((255,255,255))
                self.basic=data[3]
                self.color=WHITE
    def load_animation(self):
        
        self.standing_right=[self.sprite_list.get_image(0,0,64,64),self.sprite_list.get_image(64,0,64,64),self.sprite_list.get_image(128,0,64,64),
                            self.sprite_list.get_image(192,0,64,64),self.sprite_list.get_image(256,0,64,64)]

        for frame in self.standing_right:
            frame.set_colorkey((255,255,255))

        self.standing_left=[]
        for frame in self.standing_right:         
            self.standing_left.append(pg.transform.flip(frame,True,False))



        self.running_right=[self.sprite_list.get_image(0,64,64,64),self.sprite_list.get_image(64,64,64,64),
                            self.sprite_list.get_image(128,64,64,64),self.sprite_list.get_image(192,64,64,64),self.sprite_list.get_image(256,64,64,64),self.sprite_list.get_image(320,64,64,64)]
        for frame in self.running_right:
            frame.set_colorkey((255,255,255))
        self.running_left=[]
        for frame in self.running_right:         
            self.running_left.append(pg.transform.flip(frame,True,False))

        self.jumping_right=[self.sprite_list.get_image(0,128,64,79),self.sprite_list.get_image(64,128,64,79),self.sprite_list.get_image(128,128,64,79)]
        for frame in self.jumping_right:
            frame.set_colorkey((255,255,255))
        self.jumping_left=[]
        for frame in self.jumping_right:         
            self.jumping_left.append(pg.transform.flip(frame,True,False))
            
        self.falling_right=[self.sprite_list.get_image(0,189,64,79),self.sprite_list.get_image(64,189,64,79),self.sprite_list.get_image(128,189,64,79)]
        self.falling_left=[]
        for frame in self.falling_right:
            frame.set_colorkey((255,255,255))
        for frame in self.falling_right:         
            self.falling_left.append(pg.transform.flip(frame,True,False))
   
        self.attack_anim_right=[self.sprite_list.get_image(0,204,64,64),self.sprite_list.get_image(64,204,77,64),self.sprite_list.get_image(141,204,64,64)]
        self.attack_anim_left=[]
        for frame in self.attack_anim_right:
            frame.set_colorkey((255,255,255))
        for frame in self.attack_anim_right:         
            self.attack_anim_left.append(pg.transform.flip(frame,True,False))
    
    def animation(self):
           
            def play_animation(list,speed):

                if pg.time.get_ticks()-self.last_animation>=speed:
                    self.last_animation=pg.time.get_ticks()
                    self.frame=(self.frame+1)%len(list)
                    self.image=list[self.frame]
            speed=75
            if self.spec=="archer":
                speed=100
            if not self.attacking:
                if not self.jumping and self.walking:
                      if self.state=="right":
              
                          play_animation(self.running_right,speed)
                      elif self.state=="left":

                  
                             play_animation(self.running_left,speed)
                if not self.walking and not self.jumping:
                    if self.state=="right":
                  
                             play_animation(self.standing_right,speed)
                    elif self.state=="left":
                  
                             play_animation(self.standing_left,speed)
                if self.jumping:
                    if self.state=="right":
                
                             play_animation(self.jumping_right,speed)
                    elif self.state=="left":     
                             play_animation(self.jumping_left,speed)
                if self.falling:
                    if self.state=="right":                                    
                             play_animation(self.falling_right,speed)
                    elif self.state=="left":               
                             play_animation(self.falling_left,speed)
            if self.attacking:
                         
                         if self.state=="right":                                    
                                 play_animation(self.attack_anim_right,40)
                         elif self.state=="left":               
                                 play_animation(self.attack_anim_left,40)
                    
                
    def clear_inventory(self):
        self.inventory=[]
        self.equiped_items={'head':None,
                            'body':None,
                            'under armor':None,
                            'gloves':None,
                            'boots':None,
                            'greave':None,
                            'right hand':None,
                            'left hand':None, 
                            'both':None
                            }



  
    def throw(self):
        
        count=0

        for item in self.inventory:
                if item.name.endswith('(throwable)'):
                    current=item
                    count+=1
                    
                    break
        if count!=0:
         ms_pos=vec(pg.mouse.get_pos())
         vect=vec( self.rot.x,1)
         a=sprites.Attack(self.game,vec(self.pos.x,self.pos.y),vect,current.damage,current.type_of_damage,'grenade','enemies',w=self.rect.width,h=self.rect.height)
         for item in self.inventory:
                if item==current:
                    self.inventory.remove(item)
                    break  
                    a.acc.x+=500

    def load_conditions(self):

         if not self.attacking:
                
            if  abs(self.vel.x)<=0.3:
                  self.walking=False
            else:
                 self.walking=True
     
          
            if self.vel.y!=0:
                if self.vel.y<0:
                   self.jumping=True
                   self.falling=False
                elif self.vel.y>0:
                  self.jumping=False
                  self.falling=True
            else:
                self.jumping=False
                self.falling=False
         elif self.attacking:
             if pg.time.get_ticks()-self.begin_attack>200:
                 self.begin_attack=pg.time.get_ticks()
                 self.attacking=False
                

    def say_words(self,string,timer,time_pos,begin_time):
        now=pg.time.get_ticks()
        if pg.time.get_ticks()>=begin_time+time_pos*1000 and pg.time.get_ticks()<=begin_time+timer*1000+time_pos*1000:
            sprites.Floating_number(self.game,self.pos.x-100,self.pos.y-100,string,"words",timer)
             
         
    
    def give_start_equipment(self):
        with open(items_file) as file:
                        data=json.load(file)
        
        
        self.inventory.append(sprites.Item(self.game,self.pos.x,self.pos.y,0,True))
        self.inventory.append(sprites.Item(self.game,self.pos.x,self.pos.y,0,True))
        self.inventory.append(sprites.Item(self.game,self.pos.x,self.pos.y,1,True))
        self.inventory.append(sprites.Item(self.game,self.pos.x,self.pos.y,1,True))
        if self.spec=='warrior':
          
                 self.inventory.append(give_named_item_code("Bronze helmet",self.game))
                 self.inventory.append(give_named_item_code("Bronze chestplate",self.game))
                 self.inventory.append(give_named_item_code("iron sword",self.game))
        elif self.spec=='archer':
                 self.inventory.append(give_named_item_code("cracked bow",self.game))
                 self.inventory.append(give_named_item_code("Leather helmet",self.game))
                 self.inventory.append(give_named_item_code("Trenchcoat",self.game))
        elif self.spec=='wizard':
                 self.inventory.append(give_named_item_code("Mage's hat",self.game))
                 self.inventory.append(give_named_item_code("Beatiful gloves",self.game))
                 self.inventory.append(give_named_item_code("wooden staff",self.game))
        elif self.spec=='priest':
                 self.inventory.append(give_named_item_code("miter",self.game))
                 self.inventory.append(give_named_item_code("Black cassock",self.game))
                 self.inventory.append(give_named_item_code("Holy Bibr",self.game))
 
    def levelup(self): #повышение уровня
        if self.exp>=self.level*10: #если игрок достиг нужного кол-ва очков то
            self.exp-=self.level*10
            print("Level up!")
            print("Current level "+str(self.level))
            self.level+=1
            self.free_points+=4
            self.refresh_atributes()


      #Здоровье
    def refresh_atributes(self):

        
        self.inc_health=self.endurance*2
        self.max_health=self.basic['Basic health']+self.level*self.inc_health

        self.attack_speed=1100-self.agility*20
        if self.attack_speed<=100:
            self.attack_speed=100

        self.inc_mana=self.intelligence*2                                                  #ОПАСНО!!! БАЛАНС!!!!
        self.max_mana=self.basic['Basic mana']+self.level*self.inc_mana

        self.mana_regen=self.spirit/10
        self.health_regen=self.spirit/10
  
    def health_regeneration(self):
        if self.health<self.max_health:
            now = pg.time.get_ticks()
            if now - self.last_health_rest >= self.restore_cooldown:
                self.last_health_rest = now
                self.health+=self.health_regen

    def mana_regeneration(self):
        if self.mana<self.max_mana:
            now = pg.time.get_ticks()
            if now - self.last_mana_rest >= self.restore_cooldown:
                self.last_mana_rest = now
                self.mana+=self.mana_regen      
            
    


    
           

    def use_punch(self):                                         #ТРЕБУЕТСЯ ОБНОВЛЕНИЕ!!!!!!
            now = pg.time.get_ticks()
            if now - self.last_punch >= self.attack_speed:
                self.last_punch = now
                self.attacking=True
                self.begin_attack=pg.time.get_ticks()
                self.game.DJ.play_effect('punch')
                
                self.punch()
               
                
            
          
    def punch(self):
        
        damage=int(self.strenght*1.5+self.agility*1.2+self.weapon_damage)
        self.ability_temp('punch',0,damage)
        self.attacking=True
       
    
    def use_ability(self):
        
         if pg.time.get_ticks() - self.last_ability >= self.attack_speed:
                self.last_ability = pg.time.get_ticks()          
                if self.spec=='warrior':
                 self.warrior_ability()
                if self.spec=='archer':
                    self.archer_ability()
                   
                if self.spec=='wizard':
                    self.wizard_ability()
                if self.spec=='priest':
                    self.priest_ability()
    def use_ultimate(self):
        if self.charges_of_ultimate>0:
            
           
            if pg.time.get_ticks() - self.last_ultimate >= self.attack_speed:
                    self.last_ultimate = pg.time.get_ticks()          
                    if self.spec=='warrior':
                     self.warrior_ultimate()
                    if self.spec=='archer':
                        self.archer_ultimate()
                    if self.spec=='wizard':
                        self.wizard_ultimate()
                    if self.spec=='priest':
                        self.priest_ultimate()
                    
                    
            else:
                sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('ultimate reload'),"log")
        else:
             sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('solve'),"log")
             

    def ability_temp(self,type,manacost,damage,type_of_damage_in='physical',sound=None):                      #шаблон для способностей
        if self.mana>=manacost:
           
            wtf=len(self.game.attacks)
            if sound!=None:
              self.game.DJ.play_effect(sound)

            if type!='punch':
             
               self.list_of_attacks.append(sprites.Attack(self.game,vec(self.rect.centerx,self.rect.centery+self.shoot_pos),self.rot,damage,type_of_damage_in,type,'enemies',w=self.rect.width,h=self.rect.height))
            else:
            
              self.list_of_attacks.append(sprites.Attack(self.game,vec(self.pos.x,self.pos.y-10),self.rot,damage,type_of_damage_in,type,'enemies',w=self.rect.width,h=self.rect.height))
            lol=len(self.game.attacks)
          
            if lol>wtf:
             self.mana-=manacost
            
            
                
            if manacost!=0:
               
                sprites.Floating_number(self.game,self.pos.x,self.pos.y,"-"+str(manacost)+text('mp'),"magical")
                
               
        else:
            
            sprites.Floating_number(self.game,self.pos.x,self.pos.y,text("no mana"),"sign")
            
            
         


       

    def warrior_ability(self):
        
        damage=self.strenght*1.5+self.weapon_damage+self.agility
        self.ability_temp('punch',self.ultimate_manacost,damage)
        
    def warrior_ultimate(self):
            
            damage=self.strenght*self.agility/2+self.weapon_damage
            self.ability_temp('punch',self.ultimate_manacost,damage,'clear')
            self.charges_of_ultimate-=1
    def with_item_ends(self,how):
        for item in self.equiped_items.values():
            if item!=None:
                if item.name.endswith(how):
                    return True
                  

    def with_item_starts(self,how):
        for item in self.equiped_items.values():
            if item!=None:
                if item.name.startswith(how):
                    return True 
    def archer_ability(self):
         if self.with_item_ends('bow') or self.with_item_starts('bow'):
               damage=self.agility*2+self.weapon_damage
               self.ability_temp('arrow',self.active_manacost,damage)
         else:
           sprites.Floating_number(self.game,self.pos.x,self.pos.x,text("no bow"),"sign")
 
    def archer_ultimate(self):
        if self.mana>=self.ultimate_manacost:
            if self.with_item_ends('bow') or self.with_item_starts('bow'):
                    if self.charges_of_ultimate>0:
                        damage=self.agility*2 + self.weapon_damage
                        self.ability_temp('arrow',self.ultimate_manacost,damage,"clear")
                        self.charges_of_ultimate-=1
                    else:
                        sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('solve'),"log")
                        
                  
            else:
               sprites.Floating_number(self.game,self.pos.x,self.pos.y,text("no bow"),"sign")
       
            
            

    def wizard_ability(self):
        
        if self.equiped_items['right hand']!=None:
            if self.equiped_items['right hand'].name.endswith('staff') or self.equiped_items['right hand'].name.endswith('(staff)'):
               
                damage=self.intelligence*5+self.weapon_damage
                self.ability_temp('magic_missle',self.active_manacost,damage,'magical','magic_missle')
                

            else:
                sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('no staff'),'sign')
        else:
            sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('no staff'),'sign')
    def wizard_ultimate(self):
        
       self.charges_of_ultimate-=1
                        
              
    def priest_ability(self):
       if self.with_item_starts("Holy"):
                damage=self.spirit*1.5+self.weapon_damage+self.strenght
                self.ability_temp('punch',self.active_manacost,damage,'clear')
           
       else:
                sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('holy'),'sign')
    def priest_ultimate(self):    
        
     if self.with_item_starts("Holy"):
                
                if self.mana>self.ultimate_manacost:
                    self.mana-=self.ultimate_manacost
                    restoring=self.spirit*self.intelligence+5
                    self.health+=restoring
                    self.charges_of_ultimate-=1
                    sprites.Floating_number(self.game,self.pos.x,self.pos.y,"+"+str(restoring)+text("hp"),"physical")
                else:
                    sprites.Floating_number(self.game,self.pos.x,self.pos.y,text("no mana"),"sign")
                    
            
     else:
                sprites.Floating_number(self.game,self.pos.x,self.pos.y,text('holy'),'sign')
       
    def solve_equation(self):
         now = pg.time.get_ticks()
         if now - self.try_to_solve >= 3000:
            self.try_to_solve = now                       
            if equation_manager.equation(self):
                self.charges_of_ultimate+=3
                print("Succes! Charges +3")
                print("Current charges: "+str(self.charges_of_ultimate))
            else:

               print("Incorrect!")
   
    

    def refresh_weapon_damage(self):
        if self.equiped_items['right hand']!=None:
            if self.equiped_items['left hand']!=None and self.equiped_items['left hand'].type=='weapon':
                self.weapon_damage=self.equiped_items['right hand'].damage+self.equiped_items['left hand'].damage+self.strenght
            else:
                self.weapon_damage=self.equiped_items['right hand'].damage+self.strenght
        else:
            self.weapon_damage=self.strenght
   
    def refresh_armor(self):
        temp_armor=self.p_armor
        self.p_armor=self.basic["Basic p_armor"]
        for key,value in self.equiped_items.items():
            if value!=None:
                if value.type=='armor':
                 self.p_armor+=value.armor
        if self.p_armor!=temp_armor:
             
             if self.p_armor>temp_armor:
                 print("Your armor increased by "+str(self.p_armor-temp_armor)+" points")
             elif self.p_armor<temp_armor:
                 print("Your armor decreased by "+str(temp_armor-self.p_armor)+" points")
             
    def refresh_magic_resist(self):
        temp_armor=self.m_armor
        self.m_armor=self.basic['Basic m_armor'] 
        for key,value in self.equiped_items.items():
            try:
                if value!=None:
                    if value.type=='armor':
                     self.m_armor+=value.magic_protection
            except:
                pass
        if self.m_armor>temp_armor:
                      print("Your magical resistance increased by "+str(self.m_armor-temp_armor)+" points")
        elif self.m_armor<temp_armor:
                      print("Your magical resistance decreased by "+str(temp_armor-self.m_armor)+" points")
        
        
    def armor_update(self):
        self.refresh_armor()
        self.refresh_magic_resist()
    def subclass_initialization(self):
        self.game.player_1=SubClass(self.game,self.pos.x,self.pos.y,self.spec)
    def get_keys(self):
   
        keys = pg.key.get_pressed()
        if keys[pg.K_r] :
           self.solve_equation()
      
        if keys[pg.K_w]:
            self.near_ladder()
            self.climbing()
       
    def restrict(self):
         if self.mana>self.max_mana:
            self.mana=self.max_mana
         if self.health>self.max_health:
            self.health=self.max_health
    def save_level_result(self):
        if self.health>0:
            live=True
        else:
            live=False
        dealed_damage=0
        accuracy=0
        hits=0
        i=0
        kills=0
        for attack in self.list_of_attacks:
            i+=1
            try:
                if attack.attacked:
                    dealed_damage+=attack.total_damage                 
                    hits+=1
            except:
                pass
            try:
                if  attack.lasthit:
                    kills+=1
               
            except:
                pass
        try:

           accuracy=round((hits/i),2)
        except:
           accuracy=0
        
        with open(ANALYSIS_FOLDER+"logs\\level_result.json") as file:
            data=json.load(file)

        stats={"Name":self.nick_name,"Class":self.spec,"Level":self.level,"Dealed damage":dealed_damage,"Accuracy":accuracy,"wave":self.game.wave,"mobs killed":kills}
        data.append(stats)
        with open(ANALYSIS_FOLDER+"logs\\level_result.json",'w') as file:
            json.dump(data,file)
        
    def save_data(self,filename=saving_file):
        inventory=[]
        for item in self.inventory:
            inventory.append(item.id)
        equiped={
                 'head':None,
                 'body':None,
                 'under armor':None,
                 'gloves':None,
                 'boots':None,
                 'greave':None,
                 'right hand':None,
                 'left hand':None}
        for key,value in self.equiped_items.items():
            if value!=None:
                equiped[key]=value.id

        
        data={#"x":self.rect.x,
              #"y":self.rect.y,
              "current hp":self.health,
              "current mp":self.mana,
              "current exp":self.exp,
              "current level":self.level,
              "inventory":inventory,
              "equiped":equiped,
              "strenght":self.strenght,
              "endurance":self.endurance,
              "intelligence":self.intelligence,
              "agility":self.agility,
              "spirit":self.spirit,
              "last class":self.spec,
              "free points":self.free_points,
              "armor_type":self.armor_type,
              "rank_of_armor":self.rank_of_armor,
              "name":self.nick_name,
              "level":self.game.mapname
              
            }

        with open(filename,'w') as jf:
           json.dump(data,jf)


    def use_inventory(self):
        
        self.inv.active= not self.inv.active
        self.inv.full_update()


   

    def use_stats(self):
         self.stats.active= not self.stats.active
         self.stats.canceling()
         self.stats.full_update()
    def use(self):
         hits=pg.sprite.spritecollide(self,self.game.chests,False,False)
         if hits:
           for hit in hits:
             hit.use()
         hits=pg.sprite.spritecollide(self,self.game.buttons,False,False)
         if hits:
           for hit in hits:
             hit.activate()
    def restore_mana(self):
     if pg.time.get_ticks()- self.try_to_restore>=self.trying_timer:
        if equation_manager.equation(self):
            restoring=(self.max_mana-self.mana)/2
            self.mana+=restoring
            sprites.Floating_number(self.game,self.pos.x,self.pos.y-32,"+"+str(restoring)+text('mp'),"magical")
        else:
            self.mana-=self.mana/3
            sprites.Floating_number(self.game,self.pos.x,self.pos.y-32,"-"+str(self.mana/3)+text('mp'),"magical")
     
    def load_data(self,filename=saving_file):
        with open(basic_file) as file:
            basic_data=json.load(file)
        with open(filename) as file:
            data=json.load(file)
       # self.pos.x=data['x']
       # self.pos.y=data['y']
        
        self.health=data['current hp']
        self.mana=data['current mp']
        self.exp=data['current exp']
        self.nick_name=data['name']
        self.level=data['current level']
        self.intelligence=data['intelligence']
        self.strenght=data['strenght']
        self.endurance=data["endurance"]
        self.agility=data['agility']
        self.spirit=data['spirit']
        self.spec=data['last class']
        self.free_points=data['free points']
        self.armor_type=data['armor_type']
        self.rank_of_armor=data['rank_of_armor']
       
           
            
        self.load_images(basic_data)
        
        self.m_armor=self.basic['Basic m_armor']
        self.p_armor=self.basic["Basic p_armor"]
        
        inventory=data['inventory']
        equiped=data['equiped']
        self.inventory=[]
        self.equiped_items={}
        for item_id in inventory:
            item=sprites.Item(self.game,0,0,item_id)
            self.inventory.append(item)
            item.kill()
        for key,value in equiped.items():
            if value==None:
                self.equiped_items[key]=value
            else:
                item=sprites.Item(self.game,0,0,value)
                self.equiped_items[key]=item
                item.kill()

        self.refresh_armor()
        self.set_path()
    

  
    def multi(self):
         if len(self.game.heroes)-1==0:
             self.player_number=1
            
         elif len(self.game.heroes)-1==1:
            self.player_number=2
            
         elif len(self.game.heroes)-1==2:
            self.player_number=3
    def ways_of_control(self):
       
        
        keys = pg.key.get_pressed()
        if self.player_number==1:
           if keys[pg.K_LEFT]:
               
                    self.acc.x = -PLAYER_ACC
                    self.state='left'               
                    self.rot=vec(1,0)              
        
           if keys[pg.K_RIGHT]:
               
                    self.acc.x = PLAYER_ACC
                    self.state='right'
                    self.rot=vec(-1,0)               
            
        elif self.player_number==2:
            
           if keys[pg.K_a]:
               
                    self.acc.x = -PLAYER_ACC
                    self.state='left'               
                    self.rot=vec(1,0)              
        
           if keys[pg.K_d]:
               
                    self.acc.x = PLAYER_ACC
                    self.state='right'
                    self.rot=vec(-1,0)           
                
        elif self.player_number==3:
            if keys[pg.K_4]:
                    self.acc.x = -PLAYER_ACC
                    self.state='left'
            if  keys[pg.K_6]:
                self.acc.x = PLAYER_ACC
                self.state='right'
        
   
   
           
    def update(self):
        self.get_keys()
        self.collide_with_platforms()
       
        self.load_conditions()
        self.animation()
        if self.isStunned:
            self.image=self.laying
                    
        keys=pg.key.get_pressed()
        self.acc = vec(0, PLAYER_GRAV)
        if not self.isScene and not self.isStunned:
             self.ways_of_control()
       
         
       
            
                
        self.acc.x += self.vel.x * PLAYER_FRICTION      
        self.vel += self.acc
   
        self.pos += self.vel + 0.5 * self.acc 
        self.rect.x = self.pos.x
        self.collide('x')
        self.rect.y = self.pos.y
        self.collide('y')
        self.colliding_with_hills('y')
        self.colliding_with_hills   ('x')
        self.restrict()
       
        self.health_regeneration()
        self.mana_regeneration()
        if self.health<=0:
            self.life=False
            self.kill()
            self.save_level_result()
      
        
        self.levelup()
        
     


class SubClass(Basic):
     def __init__(self, player, x, y):
        super().__init__(player, x, y)
     