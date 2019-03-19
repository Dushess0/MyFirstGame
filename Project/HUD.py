
import pygame as pg
from settings import *
import sprites
import language_manager
vec=pg.math.Vector2

HEALTH_COLOR=(140,18,0)
MANA_COLOR=(9,50,89)
AGILITY_COLOR=(13,133,10)
EXPIERENCE_COLOR=(223,179,0)
FONT_FILE=language_manager.get_font_from_language()
def question(a):
    a=a.lower()
    if a=='y' or a=='yes' or a=='yeah' or a=='ok' or a=='ага' or a=='yep' or a=='yes of course':
        return True
    else:
        return False
class Socket():
    def __init__(self,item,rect):
        self.rect=rect
        self.item=item
        self.isactive=False
        self.hit=0
        self.isShowed=False
        self.temp=0
class Button():
    def __init__(self,x,y,width,height,type):
        self.rect=(x,y,width,height)
        self.type=type
    def get_pressed(self):
        mspos=pg.mouse.get_pos()
        mouse_x=mspos[0]
        mouse_y=mspos[1]
        if mouse_x>=self.rect[0] and mouse_x<=self.rect[0]+self.rect[2]:
            if mouse_y>=self.rect[1] and mouse_y<=self.rect[1]+self.rect[3]:
                   return True
class DoubleArrow():
    def __init__(self,x_left,y_left,x_right,y_right,width,height,atribute):
        self.rect_right=(x_right,y_right,width,height)
        self.rect_left=(x_left,y_left,width,height)
        self.atribute=atribute
        
    def get_pressed_right_arrow(self):
        mspos=pg.mouse.get_pos()
        mouse_x=mspos[0]
        mouse_y=mspos[1]
        if mouse_x>=self.rect_right[0] and mouse_x<=self.rect_right[0]+self.rect_right[2]:
            if mouse_y>=self.rect_right[1] and mouse_y<=self.rect_right[1]+self.rect_right[3]:
                   return True
    def get_pressed_left_arrow(self):
        mspos=pg.mouse.get_pos()
        mouse_x=mspos[0]
        mouse_y=mspos[1]
        if mouse_x>=self.rect_left[0] and mouse_x<=self.rect_left[0]+self.rect_left[2]:
            if mouse_y>=self.rect_left[1] and mouse_y<=self.rect_left[1]+self.rect_left[3]:
                   return True
    def set_temp(self,atribute):
        self.temp=atribute

class Inventory_HUD(pg.sprite.Sprite):

    def __init__(self, game, x, y,hero):

        self.groups = game.HUD_components
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game=game
        
        self.image = pg.image.load(HUD_inventory_file)               
        self.active=False
        self.rect = self.image.get_rect()
        self.font=language_manager.get_font_from_language()
        self.pos=vec(x,y)
        
        self.left_arrow_cords=(280,425,70,50)
        self.right_arrow_cords=(360,425,70,50)
        self.sockets=[]
        self.paper=1
        self.start_point_x=70
        self.start_point_y=140
        self.name_x=400
        self.name_y=570
        self.info_main_x=40
        self.info_main_y=610
        self.equiped_x=600
        self.equiped_y=140
     
        self.info_mid_x=415
       

        self.sockets_equiped=[]
        self.last_item=None
        self.last_sign=pg.time.get_ticks()
        self.hero=hero
        self.last_drawing=0
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
    def full_update(self):
        self.update_equiped()       
        self.update_sockets_equiped()
        self.update_inventory()
        self.update_sockets()
    def timer(self,seconds):
       now=pg.time.get_ticks()
       if now -self.last_sign>=seconds*1000:
           self.last_sign=now
           return True
        
      
        
    def get_pressed(self,arrow):
        
                mspos=pg.mouse.get_pos()
                if mspos[0]>=arrow[0] and mspos[0]<=arrow[0]+arrow[2]:
                    if mspos[1]>=arrow[1]  and mspos[1]<=arrow[1]+arrow[3]:               
                         return True

    def get_pressed_left_arrow(self):
        if self.get_pressed(self.left_arrow_cords):

             return True
       
    def get_pressed_right_arrow(self):
        if self.get_pressed(self.right_arrow_cords):
            return True
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):

        font = pg.font.Font(font_name, size)

        text_surface = font.render(text,0,color)

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

        self.image.blit(text_surface, text_rect)

    def update_inventory(self):
        
            self.inventory=self.hero.inventory
            self.clear()
    def update_equiped(self):
        self.equiped=[]
        
        for item in self.hero.equiped_items.values():
                if item!=None:             
                    self.equiped.append(item)
        
        self.clear()
    def update_sockets_equiped(self):
        self.sockets_equiped=[]
        height=30
        width=200
        i=0
        
        for item in self.equiped:
            socket=Socket(item,(self.equiped_x,self.equiped_y+i*height,width,height))
            self.sockets_equiped.append(socket)
            
            i+=1
    def mouse_on_inventory(self):
        mspos=vec(pg.mouse.get_pos())
        i=0
        item=None
        
        for socket in self.sockets:
             if  self.get_pressed(socket.rect):
               item=socket.item
               i=1
               break
        if i==1 and item!=None:
            return item
        else:
           return False
    def mouse_on_equiped(self):
        mspos=vec(pg.mouse.get_pos())
        i=0
        item=None
        
        for socket in self.sockets_equiped:
             if  self.get_pressed(socket.rect):
               item=socket.item
               i=1
               break
        if i==1 and item!=None:
            return item
        else:
           return False
             
    def update_sockets(self):
        self.sockets=[]
        i=0
        
        height=30
        width=200
        if self.paper==1:
           for item in self.inventory[:10]:
            socket=Socket(item,(self.start_point_x,self.start_point_y+i*height,width,height))
            self.sockets.append(socket)
            i+=1
        elif self.paper==2:
            for item in self.inventory[10:]:
             socket=Socket(item,(self.start_point_x,self.start_point_y+i*height,width,height))
             self.sockets.append(socket)
             i+=1


    def  draw_information(self):
        def draw(item):
                self.draw_text(item.name,self.font,25,BLACK,self.name_x,self.name_y)

                self.draw_text("Level: "+str(item.level),self.font,20,BLACK,self.info_main_x,self.info_main_y)
                self.draw_text("Rarity : "+item.rarity,self.font,20,BLACK,self.info_main_x,self.info_main_y+spacing*1)
                if item.rarity=='usual':
                       COLOR=BLACK
                elif item.rarity=='rare':
                     COLOR=MANA_COLOR
                elif item.rarity=='unique':
                    COLOR=AGILITY_COLOR
                elif item.rarity=='legendary':
                    COLOR=YELLOW
                elif item.rarity=='epic':
                     COLOR=(146,0,209)
                self.draw_text("Type : "+item.type,self.font,20,COLOR,self.info_main_x,self.info_main_y+spacing*2)


               
                if item.type=='armor':
                  self.draw_text("Physical protection : "+str(item.armor),self.font,20,BLACK,self.info_mid_x,self.info_main_y)
                  self.draw_text("Magical resistance : "+str(item.magic_protection),self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing*1)
                  self.draw_text("Part of body :"+str(item.part),self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing*2)
                  self.draw_text("Type :"+item.weight,self.font,20,BLACK,self.info_main_x,self.info_main_y+spacing*3)
                  if item.isHoly:
                        self.draw_text("This armor is blessed by God",self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing*3)            
                if item.type=='weapon':
                  self.draw_text("Damage : "+str(item.damage),self.font,20,BLACK,self.info_mid_x,self.info_main_y)
                  self.draw_text("Part of body : "+str(item.part),self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing*1)
                  if item.isHoly:
                        self.draw_text("This weapon is blessed by Gods",self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing*2)

                if item.type=='potion':
                  if item.action=='health':
                      color=HEALTH_COLOR
                  elif item.action=='mana':
                      color=MANA_COLOR
                  self.draw_text("Restoring : "+str(item.action),self.font,20,BLACK,self.info_mid_x,self.info_main_y)
                  self.draw_text("Restoration :"+str(item.restoring),self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing)        
              
                  if item.isHoly:
                        self.draw_text("This potion is blessed by Gods",self.font,20,BLACK,self.info_mid_x,self.info_main_y+spacing*2)  
              
                        

        spacing=25
       
        if self.mouse_on_inventory()!=False:
            item=self.mouse_on_inventory()
            if item!=self.last_drawing:
                self.last_drawing=item
                self.clear()
            draw(item)
        elif self.mouse_on_equiped()!=False:
            item=self.mouse_on_equiped()
            if item!=self.last_drawing:
                self.last_drawing=item
                self.clear()
            draw(item)


     

    def draw_items(self):
        
        if self.paper==1:
            i=0
            spacing=30          
            for socket in self.sockets[:10]:
            
                self.draw_text(socket.item.name,self.font,20,BLACK,self.start_point_x,self.start_point_y+i*spacing)             
                i+=1    
        elif self.paper==2:
            i=0
            spacing=30                  
            for socket in self.sockets[:20]:             
               self.draw_text(socket.item.name,self.font,20,BLACK,self.start_point_x,self.start_point_y+i*spacing)             
               i+=1
    def draw_total_protection(self):
        
            self.draw_text(str(self.hero.m_armor),self.font,15,(51,51,51),942,445)
            self.draw_text(str(self.hero.p_armor),self.font,15,(0,0,255),942,460)
    def draw_equiped(self):
            i=0
            spacing=30
            for socket in self.sockets_equiped:
                
                self.draw_text(socket.item.name+" as "+socket.item.part,self.font,18,BLACK,self.equiped_x,self.equiped_y+i*spacing)             
                i+=1    
    def equip(self,choosen_item):
        
            if choosen_item.part=='both':
                                     if self.hero.equiped_items['right hand']==None and self.equiped_items['left hand']==None and self.equiped_items['both']==None:
                                         self.hero.equiped_items['both']=choosen_item
                                         self.hero.inventory.remove(choosen_item)
                                         print("Equiped as two-handed weapon : "+choosen_item.name)
                                     else:
                                       print("Please free your hands!")
            else:
                             for key,value in self.hero.equiped_items.items():                 
                                 if key==choosen_item.part:
                                     if value==None:

                                         if choosen_item.type=='armor':
                                            if self.hero.rank_of_armor>=choosen_item.weight_int:
                                            
                                                    if choosen_item.iscursed:
                                                      a=input("Are you sure? You want to equip cursed item ? Y/N ")
                                                      if question(a):
                                                            self.hero.equiped_items[key]=choosen_item
                                                            print("Armor "+choosen_item.name+" equiped as "+choosen_item.part)
                                                            self.hero.inventory.remove(choosen_item)
                                                            print("YOU EQUIPED CURSED ITEM!!")
                                                    elif choosen_item.iscursed==False:
                                                           self.hero.equiped_items[key]=choosen_item
                                                           print("Armor "+choosen_item.name+" equiped as "+choosen_item.part)
                                                           self.hero.inventory.remove(choosen_item)
                                               
                                            else:
                                               print("You are too weak!")
                                               
                                            
                                         elif choosen_item.type=='weapon':
                                            self.hero.equiped_items[key]=choosen_item
                                            print("Weapon "+choosen_item.name+" equiped as "+choosen_item.part)
                                            self.hero.inventory.remove(choosen_item)
                                            if choosen_item.iscursed:
                                                print("You equiped cursed weapon!")
                                 
                                     else:
                                         print("This part of equipment is already dressed ")                               
            self.hero.armor_update()                          
                                    


                
    def drop(self,item):              #выбросить
            for socket in self.sockets:
                if socket.item.name==item.name:
                    self.sockets.remove(socket)
                    self.hero.inventory.remove(item)
            
    def unequip(self,socket):
            item=socket.item
        
            if len(self.hero.inventory)<self.hero.inventory_capacity:
                if item.iscursed:
                    print("You cant remove this!")
                else:
                    self.hero.equiped_items[item.part]=None
                    self.hero.inventory.append(item)
                    self.equiped.remove(item)
                
            else:
                print("Your inventory is full")
            self.hero.armor_update()
            self.full_update()
    def use_potion(self,choosen_potion):
       
            if choosen_potion.action=='health':
                        self.hero.health+=choosen_potion.restoring
                        self.hero.inventory.remove(choosen_potion)
            elif choosen_potion.action=='mana':
                        self.hero.mana+=choosen_potion.restoring
                        self.hero.inventory.remove(choosen_potion)
            self.full_update()
         
    def clear(self):
        self.image = pg.image.load(HUD_inventory_file)
    def interaction(self,code):
        if code==1:
            if self.get_pressed_left_arrow():
                if self.paper!=1:
                    self.paper-=1          
            elif self.get_pressed_right_arrow():
                if self.paper!=2:
                  self.paper+=1
            for socket in self.sockets:  
              if self.get_pressed(socket.rect):
                   socket.isactive=True
                #   print(socket.item.name)
              else:
                  socket.isactive=False
            for socket in self.sockets_equiped:
                if self.get_pressed(socket.rect):
                   socket.isactive=True
                #   print(socket.item.name)
                else:
                  socket.isactive=False
        

        elif code==3:
            for socket in self.sockets:

                if self.get_pressed(socket.rect):
                   
                    if socket.item.type=='armor' or socket.item.type=='weapon':           
                      self.equip(socket.item)     
                      self.hero.refresh_weapon_damage()
                      self.hero.refresh_armor()
                    elif socket.item.type=='potion':
                        self.use_potion(socket.item)
            for socket in self.sockets_equiped:
                 if self.get_pressed(socket.rect):
                  self.unequip(socket)
                  
        elif code==2:
           
            for socket in self.sockets:
                
                 if self.get_pressed(socket.rect):
                           item=socket.item
                           a=input("You really want to drop "+item.name+"? ")
                           if question(a):
                               self.drop(socket.item)
                               print("Succesfully droped: "+item.name)
                           else:
                               print(item.name+" remains in your inventory!")
        self.full_update()
        self.clear()
                
           
        
        
    def draw(self):
        self.game.screen.blit(self.image, ( self.pos.x,self.pos.y))
       
    def update(self):
        if self.active:
         self.draw_information()
         self.draw_items()
         self.draw_equiped()
         self.draw_total_protection()
         for socket in self.sockets:
            if  socket.isactive:
                print(sockets.item.name)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

    if pct > 0.6:
        col = (53,156,37)
    elif pct > 0.3:
        col = (195,182,0)
    else:
        col = (127,13,0)

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, (115,7,7), outline_rect, 2)
def draw_player_icon(screen,icon,pos):
    rect=pg.Rect(pos.x,pos.y,10,10)
    screen.blit(icon,rect)
    

def draw_player_mana(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

    if pct > 0.6:
        col = (8,35,127)
    elif pct > 0.3:
        col = (55,86,186)
    else:
        col = (115,131,181)

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, (0,59,252), outline_rect, 2)

def draw_player_exp(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

    col=(223,179,0)

    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, (245,184,18), outline_rect, 2)

def show_information_log(hit):
             print()
             
          
             print("Short information")
             print("Level of item "+str(hit.level))
             print("Type of item "+hit.type)
             print("Rarity: "+hit.rarity)
             if hit.type=='armor':
                 print("Rank of armor "+str(hit.armor))
                 print("Type of armor "+hit.weight)
             if hit.type=='weapon':
                 print("Damage "+str(hit.damage))
             if hit.type=='armor' and hit.type=='weapon':
              print("Part of body "+hit.part)
             if hit.type=='potion':
                 if hit.action=='health':
                  print("This potion can restore "+str(hit.restoring)+" hp")
                 elif hit.action=='mana':
                     print("This potion can restore "+str(hit.restoring)+" mp")
             
             print()





class Stats_HUD(pg.sprite.Sprite):

    def __init__(self, game, x, y,hero):

        self.groups = game.HUD_components
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game=game
        
        self.image = pg.image.load(STATS_FILE)               
        self.active=False
        self.rect = self.image.get_rect()
        self.player=hero
        self.hint=pg.image.load(HUD_hint_file)
        
        self.pos=vec(x,y)

        self.clear_timer=2000
        self.last_clear=pg.time.get_ticks()

        self.load_active_description()
        if self.player.spec=='warrior' or self.player.spec=='wizard' or self.player.spec=='archer' or self.player.spec=='priest':
            self.passive_blocked=True
        if not self.passive_blocked:
            self.load_passive_description()
        self.load_ultimate_description()


        self.strenght_buttons=DoubleArrow(871,373,909,373,22,25,"strenght")
        self.agility_buttons=DoubleArrow(871,412,909,412,22,25,"agility")
        self.intelligence_buttons=DoubleArrow(871,452,909,452,22,25,"intelligence")
        self.spirit_buttons=DoubleArrow(871,493,909,492,22,25,"spirit")
        self.endurance_buttons=DoubleArrow(871,337,909,337,22,25,"endurance")
        self.stat_buttons=[self.strenght_buttons,self.agility_buttons,self.intelligence_buttons,self.spirit_buttons,self.endurance_buttons]
       

        self.temp_strenght=0
        self.temp_agility=0
        self.temp_intelligence=0
        self.temp_spirit=0
        self.temp_endurance=0


        self.drawable_strenght=self.player.strenght+self.temp_strenght
        self.drawable_agility=self.player.agility+self.temp_agility
        self.drawable_intelligence=self.player.intelligence+ self.temp_intelligence
        self.drawable_spirit=self.player.spirit+self.temp_spirit
        self.drawable_endurance=self.player.endurance+self.temp_endurance
        self.saving_button=Button(843,538,141,45,'save')
        self.canceling_button=Button(680,538,143,45,'cancel')
        self.active_buttons=(self.saving_button,self.canceling_button)

    def update_drawable_stats(self):
        self.drawable_strenght=self.player.strenght+self.temp_strenght
        self.drawable_agility=self.player.agility+self.temp_agility
        self.drawable_intelligence=self.player.intelligence+ self.temp_intelligence
        self.drawable_spirit=self.player.spirit+self.temp_spirit
        self.drawable_endurance=self.player.endurance+self.temp_endurance
    def load_active_description(self):
        with open(languages_folder+language_manager.get_language()+DESCRIPTION_FOLDER+"active_"+str(self.player.spec)+".txt") as file:
            content=file.readlines()
        self.active_description=[]
        for line in content:
            self.active_description.append(line.rstrip())
            
    def load_passive_description(self):
        with open(languages_folder+language_manager.get_language()+DESCRIPTION_FOLDER+"passive_"+str(self.player.spec)+".txt") as file:
            content=file.readlines()
        self.passive_description=[]
        for line in content:
            self.passive_description.append(line.rstrip())
    def load_ultimate_description(self):
        with open(languages_folder+language_manager.get_language()+DESCRIPTION_FOLDER+"ultimate_"+str(self.player.spec)+".txt") as file:
            content=file.readlines()
        self.ultimate_description=[]
        for line in content:
            self.ultimate_description.append(line.rstrip())
    def clock_clear(self):
        now = pg.time.get_ticks()
        if now - self.last_clear>=self.clear_timer:
            self.last_clear=now
            self.clear()
    def full_update(self):
        self.clear()
        self.update_drawable_stats()
    
    def clear(self):
        self.image=pg.image.load(STATS_FILE)
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):

        font = pg.font.Font(font_name, size)

        text_surface = font.render(text,0,color)

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

        self.image.blit(text_surface, text_rect)
    def draw_text_on_surface(self,surface, text, font_name, size, color, x, y, align="nw"):

        font = pg.font.Font(font_name, size)

        text_surface = font.render(text,0,color)

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

        surface.blit(text_surface, text_rect)
    def draw_substats(self):
        self.update_drawable_stats
        self.draw_text(str(self.player.strenght+self.temp_strenght),FONT_FILE,18,RED,848,378)
        self.draw_text(str(self.player.agility+self.temp_agility),FONT_FILE,18,AGILITY_COLOR,848,417)
        self.draw_text(str(self.player.intelligence+self.temp_intelligence),FONT_FILE,18,MANA_COLOR,848,460)
        self.draw_text(str(self.player.spirit+self.temp_spirit),FONT_FILE,18,BLACK,848,495)
        self.draw_text(str(self.player.endurance+self.temp_endurance),FONT_FILE,18,HEALTH_COLOR,848,337)
    def saving(self):
        self.player.strenght+=self.temp_strenght
        self.player.agility+=self.temp_agility
        self.player.intelligence+=self.temp_intelligence
        self.player.spirit+=self.temp_spirit
        self.player.endurance+=self.temp_endurance

        
        self.temp_strenght=0
        self.temp_agility=0
        self.temp_intelligence=0
        self.temp_spirit=0
        self.temp_endurance=0
        print(str(self.player.free_points))
    def canceling(self):
         self.player.free_points+=self.temp_strenght+self.temp_agility+self.temp_intelligence+self.temp_spirit+self.temp_endurance      
         self.temp_strenght=0
         self.temp_agility=0
         self.temp_intelligence=0
         self.temp_spirit=0
         self.temp_endurance=0
    def interaction(self,code):
        if code==1:
            for button in self.stat_buttons:
                if button.get_pressed_right_arrow():
                    if self.player.free_points>0:
                        self.player.free_points-=1
                        if button.atribute=='strenght':
                            self.temp_strenght+=1
                            
                        elif button.atribute=='agility':
                            self.temp_agility+=1
                        elif button.atribute=='intelligence':
                            self.temp_intelligence+=1
                        elif button.atribute=='spirit':
                            self.temp_spirit+=1
                        elif button.atribute=='endurance':
                            self.temp_endurance+=1
                  
                elif button.get_pressed_left_arrow():
                        
                        if button.atribute=='strenght':
                            if self.temp_strenght>0:
                             self.temp_strenght-=1
                             self.player.free_points+=1

                        elif button.atribute=='agility':
                            if self.temp_agility>0:
                             self.temp_agility-=1
                             self.player.free_points+=1
                        elif button.atribute=='intelligence':
                           if self.temp_intelligence>0:
                             self.temp_intelligence-=1
                             self.player.free_points+=1
                        elif button.atribute=='spirit':
                            if self.temp_spirit>0:
                             self.temp_spirit-=1
                             self.player.free_points+=1
                        elif button.atribute=='endurance':
                            if self.temp_endurance>0:
                             self.temp_endurance-=1
                             self.player.free_points+=1
            for button in self.active_buttons:
                if button.get_pressed():
                    if button.type=='save':
                        self.saving()
                        self.player.refresh_atributes()
                      
                    elif button.type=='cancel':                       
                       self.canceling()
        
        self.full_update()       
    def draw_player_mana(self, x, y, pct):
        surf=self.image
        if pct < 0:
            pct = 0
        BAR_LENGTH = 235
        BAR_HEIGHT = 16
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

        if pct > 0.6:
            col = (8,35,127)
        elif pct > 0.3:
            col = (55,86,186)
        else:
            col = (115,131,181)

        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, (0,59,252), outline_rect, 2)
    #def floating_hint(self):

    #    hint_surf=self.clear_hint

    #    mspos=pg.mouse.get_pos()
    #    self.draw_text_on_surface(hint_surf,)
        

    def draw_player_health(self, x, y, pct):
        surf=self.image
        if pct < 0:
            pct = 0
        BAR_LENGTH = 235
        BAR_HEIGHT = 16
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

        if pct > 0.6:
            col = (53,156,37)
        elif pct > 0.3:
            col = (195,182,0)
        else:
            col = (127,13,0)

        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, (115,7,7), outline_rect, 2)
    def draw_player_exp(self, x, y, pct):
        surf=self.image
        if pct < 0:
            pct = 0
        BAR_LENGTH = 235
        BAR_HEIGHT = 16
        fill = pct * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

        

        pg.draw.rect(surf, EXPIERENCE_COLOR, fill_rect)
        pg.draw.rect(surf, (245,184,18), outline_rect, 2)
    
    def show_float_with_text(self,content,spacing,size):
         i=0
         self.hint=pg.image.load(HUD_hint_file)
         for line in content:   
              self.draw_text_on_surface(self.hint,line,READABLE_FONT,size,BLACK,5,10+spacing*i)
              i=i+1
         self.image.blit(self.hint,(656,640))

    def draw_hint(self):
        code=self.show_hint()
        if code!=None:
             with open(languages_folder+language_manager.get_language()+"\\"+"hints\\"+code+".txt") as file:
               content=file.readlines()
             self.show_float_with_text(content,5,15)

    def desc_draw_temp(self,lines,startpos_x,startpos_y,size):
        
        spacing=size
        i=0
        for line in lines:   
         self.draw_text(line,READABLE_FONT,size,BLACK,startpos_x,startpos_y+spacing*i)
         i=i+1
    def draw_description(self):
        self.desc_draw_temp(self.active_description,50,285,16)
        self.desc_draw_temp(self.ultimate_description,50,450,16)
        if not self.passive_blocked:
         self.desc_draw_temp(self.passive_description,50,640,16)
    def draw_difference(self):
        
        if self.temp_strenght>0:
            self.draw_text("+"+str(self.temp_strenght),FONT_FILE,19,RED,965,373)
            
        if self.temp_agility>0:
            self.draw_text("+"+str(self.temp_agility),FONT_FILE,19,AGILITY_COLOR,965,413)
        if self.temp_intelligence>0:
           self.draw_text("+"+str(self.temp_intelligence),FONT_FILE,19,MANA_COLOR,965,453)
        if self.temp_spirit>0:
            self.draw_text("+"+str(self.temp_spirit),FONT_FILE,19,BLACK,965,495)

        if self.temp_endurance>0:
            self.draw_text("+"+str(self.temp_endurance),FONT_FILE,19,HEALTH_COLOR,965,333)

    def draw_free_points(self):
        self.draw_text(str(self.player.free_points),FONT_FILE,12,BLACK,765,304)
    def draw_numbers(self):
        self.draw_text("max "+str(self.player.max_health),FONT_FILE,16,HEALTH_COLOR,225,36)
        self.draw_text("max "+str(self.player.max_mana),FONT_FILE,16,MANA_COLOR,225,86)
        self.draw_text("need "+str(self.player.level*10),FONT_FILE,16,EXPIERENCE_COLOR,140,178)
    def draw(self):
        self.game.screen.blit(self.image, ( self.pos.x,self.pos.y))
    def show_hint(self):
        
        mspos=vec(pg.mouse.get_pos())
        #print(mspos)
        if mspos.x>=680:
            if mspos.x<=800 and mspos.y>=380 and mspos.y<=400:
                code="strenght"
                return code
                
            elif mspos.x<=776 and mspos.y>=420 and mspos.y<=434:
                code="agility"
                return code
            elif mspos.x<=840 and mspos.y>=456 and mspos.y<=477:
                code="intelligence"
                return code
            elif mspos.x<=748 and mspos.y>=500 and mspos.y<=518:
                code="spirit"
                return code
            elif mspos.x<=820 and mspos.y>=339 and mspos.y<=356:
                code="endurance"
                return code
          

    def draw_main_stats(self):
        self.clock_clear()
        self.draw_player_health(65,60,self.player.health/self.player.max_health)
        self.draw_player_mana(65,110,self.player.mana/self.player.max_mana)
        self.draw_player_exp(65,165,self.player.exp/(self.player.level*10))
        if len(str(self.player.level))==1:
          levelpos_x=415
        elif len(str(self.player.level))==2:      
          levelpos_x=405
        else:
            levelpos_x=400
        self.draw_text(str(self.player.level),FONT_FILE,25,EXPIERENCE_COLOR,levelpos_x,158)
        startpos=(365,80)
        if self.player.spec=="warrior":
            color=(128,128,128)
            startpos=(360,80)
        elif self.player.spec=="archer":
            color=(13,133,10)
        elif self.player.spec=="wizard":
            color=(9,50,89)
        elif self.player.spec=="priest":
            color=BLACK
            startpos=(370,80)
        self.draw_text(self.player.spec.upper(),FONT_FILE,25,color,startpos[0],startpos[1])

    def update(self):
        if self.active:  
          
          self.draw_main_stats()
          self.draw_description()
          self.draw_substats()
          self.draw_difference()
          self.draw_free_points()
          self.draw_numbers()
          self.draw_hint()
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y






class CutScene_part(pg.sprite.Sprite):
    def __init__(self, game, pos,hero):
        self.groups = game.HUD_components
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image=pg.Surface((WIDTH,HEIGHT/3))
        self.image.fill(BLACK)
        self.pos=pos
        self.rect=self.image.get_rect()
        self.active=False
      
        self.rect.x=self.pos.x
        self.rect.y=self.pos.y
        self.drawing_area=(350,20,625,196)
   
    def show_text(strokes,duration):
        i=0
        spacing=20
        for stroke in strokes:
         Floating_number(self.game,self.drawing_area[0]+spacing*i,self.drawing_area[1]+spacing*i,stroke,"words",duration)

    def draw(self):
        self.game.screen.blit(self.image, ( self.pos.x,self.pos.y))

    def update(self):
       
        self.rect.x=self.pos.x
        self.rect.y=self.pos.x




def draw_bar(game):
           num_of_player=0
           for player in game.heroes:
                       
                       draw_player_health(game.screen,80+200*num_of_player+10,20,player.health/player.max_health)
                       draw_player_mana(game.screen,80+200*num_of_player+10,50,player.mana/player.max_mana)
                       draw_player_exp(game.screen,80+200*num_of_player+10,80,player.exp/(player.level*10))
                       draw_player_icon(game.screen,player.icon,vec(15,15))
                       num_of_player+=1


def draw_HUD_of_players(game):   
               for hero in game.heroes:
                   if hero.inv.active and not hero.stats.active:      
                       hero.inv.draw()
                       hero.inv.pos=vec(0,0)
                       hero.stats.pos=vec(-1000000,-1000000)
                   elif hero.stats.active:
                       hero.stats.draw()
                       hero.stats.pos=vec(0,0)
                       hero.inv.pos=vec(-1000000,-1000000)
                   else:
                       hero.inv.pos=vec(-1000000,-1000000)
                       hero.stats.pos=vec(-1000000,-1000000)
                   if hero.cutscene_down.active:
                       
                       hero.cutscene_down.draw()
                       hero.cutscene_up.draw()
                       hero.cutscene_down.pos=vec(0,512)
                       hero.cutscene_up.pos=vec(0,0)
                       hero.inv.active=False
                       hero.stats.active=False
                       hero.cutscene_up.active=True

                       draw_player_icon(game.screen,hero.icon,vec(101.5,101.5))

                       game.draw_text(hero.nick_name,READABLE_FONT,20,hero.color,90,180,)

                   else:
                     hero.cutscene_down.pos=vec(-1000000,-1000000)
                     hero.cutscene_up.pos=vec(-1000000,-1000000)

def draw_in_scene(game):
     for sprite in game.heroes:           
             game.screen.blit(sprite.image,game.camera.apply(sprite))
     for sprite in game.attacks:           
             game.screen.blit(sprite.image,game.camera.apply(sprite))
     for sprite in game.enemies:           
             game.screen.blit(sprite.image,game.camera.apply(sprite))
     for sprite in game.actors:           
             game.screen.blit(sprite.image,game.camera.apply(sprite))
     



def check_for_draw(player):
     if not player.inv.active and not player.stats.active and not player.cutscene_down.active:
         return True
     else:
         False

       
              
      
       
       
      