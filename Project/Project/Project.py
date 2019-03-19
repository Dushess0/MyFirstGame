
import pygame as pg
import basic
import sys
from settings import *
import random
from tilemap import *
from sprites import *
import datetime
from os import path
import music_manager
import HUD
import language_manager
import analysis

def launch_iterator():
    with open("launches.json") as file:
        data=json.load(file)
    data["launches"]+=1
    with open("launches.json",'w') as file:
        json.dump(data,file)



def controlling(event,player):
    if player.alive():
              if not  player.isStunned and player.isScene==False:
                  if event.key==pg.K_SPACE or event.key==pg.K_UP:
                                player.jump()
               
                  if event.key==pg.K_c:
                        player.use_punch()
                  if event.key==pg.K_x:
                        player.use_ability()
                  if event.key==pg.K_v:
                        player.throw()
                  if event.key==pg.K_m:
                        player.restore_mana()
                  if event.key==pg.K_p:
                              player.use_stats()
                  if event.key==pg.K_i:
                                player.use_inventory()
                  if event.key==pg.K_e:
                                player.use_chests()
                  if event.key==pg.K_z:                  
                             player.use_ultimate()
                  if event.key==pg.K_h:                  
                              player.cutscene_down.active=not  player.cutscene_down.active
                      
                  if event.key==pg.K_t:
                     print(str(len(player.game.enemies)))

class Operator():
    def __init__(self,game):
        
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT),pg.HWSURFACE | pg.DOUBLEBUF)
        self.mapname=level_1
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
       
        pg.key.set_repeat(500, 100)

        
        self.running=True
       
        
        self.image = pg.image.load(HUD_main_menu_file)               
        self.active=False
        self.rect = self.image.get_rect()
        self.font=language_manager.get_font_from_language()
        self.pos=vec(x,y)
        self.name_rect=(222,100,595,100)
        self.new_game_rect=(384,339,271,76)
        self.load_rect=(384,407,271,76)
        self.load_exist_rect=(384,595,271,76)
        self.infinity_rect=(0,688,320,80)
        self.tips_rect=(775,688,249,80)
        self.settings_rect=(960,0,64,64)
        self.active=True
        self.game_input=game
        
       

    def get_pressed(self):
        mspos=pg.mouse.get_pos()
        mouse_x=mspos[0]
        mouse_y=mspos[1]
        if mouse_x>=self.rect[0] and mouse_x<=self.rect[0]+self.rect[2]:
            if mouse_y>=self.rect[1] and mouse_y<=self.rect[1]+self.rect[3]:
                   return True



 
    def load_exist_game(self):
        try:
            with open(saving_file) as file:
                saving=json.load(file)
            self.game_controlled(saving["level"])
            self.game_main.running=False
  
        except FileNotFoundError:
            print("No saved game")
    def interaction(self,code):
        
        if code==1:
            if self.get_pressed(self.new_game_rect):
                self.active=False
            elif self.get_pressed(self.load_exist_rect):
                 self.load_exist_game()
            else:
                print("miss")
        
               
                   
                  
               
                        
                        
            
    def update(self):
       self.rect.x=self.pos.x
       self.rect.y=self.pos.y
       if self.acive:
           self.interaction()



class Game:

    def __init__(self,mapname,DJ,wave,pack=[],mode="infinity",):

        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.mode=mode
        self.screen = pg.display.set_mode((WIDTH, HEIGHT),pg.HWSURFACE | pg.DOUBLEBUF)
        self.mapname=mapname
        pg.display.set_caption(TITLE)
        self.wave=wave
        self.clock = pg.time.Clock()
       
        self.necrologue_list=[]
        pg.key.set_repeat(500, 100)
        self.pack=pack
        self.load_data(mapname)
        self.running=True
        self.end=False
        self.DJ=DJ
        self.spawns=0
    
    def load_data(self,mapname):

      

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        
        
        self.map = Tilemap(path.join(map_folder, mapname))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        

   
    def write_necrologue(self):
        for dictionary in self.necrologue_list:
            try:
             with open(ANALYSIS_FOLDER+"logs\\mob_efficiency.json") as file:
                    data=json.load(file)
             data.append(dictionary)
             with open(ANALYSIS_FOLDER+"logs\\mob_efficiency.json",'w') as file:
                    json.dump(data,file)
            except:
                pass
    def new(self):

        # загрузка всего
        launch_iterator()
        self.all_sprites = pg.sprite.Group()

        self.walls = pg.sprite.Group()
        self.platforms=pg.sprite.Group()
        self.enemies=pg.sprite.Group()
        
        self.heroes=pg.sprite.Group()
        self.traps=pg.sprite.Group()
        self.buttons=pg.sprite.Group()
        self.ladders=pg.sprite.Group()
        self.items=pg.sprite.Group()
        self.chests=pg.sprite.Group()
        self.hints=pg.sprite.Group()
        self.attacks=pg.sprite.Group()
        self.text=pg.sprite.Group()
        self.actors=pg.sprite.Group()
        self.HUD_components=pg.sprite.Group()
        
        
        for tile_object in self.map.tmxdata.objects:
            try:
             if tile_object.spawn=="boss":
                 boss=vec(tile_object.x,tile_object.y)
                 
             elif tile_object.spawn=="miniboss":
                  miniboss=vec(tile_object.x,tile_object.y)
                  
            except:
               pass
        
          
       

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name=='Player':
                self.player_1=basic.Basic(self,tile_object.x,tile_object.y,)
                
                
            if tile_object.name.startswith('wall'):
                if tile_object.name.endswith("ice"):
                    Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height,True)
                else:
                    Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)

            if tile_object.name.startswith('platform'):
                       if tile_object.name.endswith('ice'):
                          Platform(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height,True)
                       else:
                          Platform(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
             
                
            if tile_object.name=='spawn':
                
                     
                     self.spawn_enemy(self.pack,tile_object.x,tile_object.y,boss,miniboss)
                
            if tile_object.name=="platform":
                Platform(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name=='bow':
                Item(self,tile_object.x,tile_object.y,4)
            if tile_object.name=='sword':
                Item(self,tile_object.x,tile_object.y,2)
            if tile_object.name=='staff':
                Item(self,tile_object.x,tile_object.y,3)
            if tile_object.name=='incessory':
                Item(self,tile_object.x,tile_object.y,5)
            if tile_object.name.startswith("hidden_item_"):
                Item(self,tile_object.x,tile_object.y,int(tile_object.name[-3:]),False,True)
            if tile_object.name=='ladder':
                Ladder(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)

            if tile_object.name.startswith('ENEMY'):
                list=tile_object.name.split("_")
                name=list[1]
                Enemy(self,tile_object.x,tile_object.y,name,1)
            if tile_object.name=='rand_usual':
              
                Item(self,tile_object.x,tile_object.y,0,rand_rarity='usual')

            if tile_object.name.startswith("trap"):           
                     list=tile_object.name.split("_")
                     type=list[1]
                     Trap(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height,type)
                     
                
            if tile_object.name.startswith('words'):
                Floating_number(self,tile_object.x,tile_object.y,tile_object.name[-2:],"permanent words")
            if tile_object.name.startswith('actor_'):
                  Actor(self,tile_object.x,tile_object.y,tile_object.name[-2:])
            
            if tile_object.name.startswith('chest'):
                 list=tile_object.name.split("_")
                 type=list[1]
                 Chest(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height,type)
           

            if tile_object.name.startswith('hint'):
                Hint(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height,tile_object.name)

        self.camera=Camera(self.map.width,self.map.height)
        self.current_actor=self.player_1
        
        
    def spawn_enemy(self,global_pack,pos_X,pos_Y,boss,miniboss):
        to_load=[]
        self.spawns+=1
        
        for enemy in global_pack:
            
            to_load.append({"type":enemy["type"],"level":enemy["level"],"amount":(enemy["amount"]/self.spawns)})
           
        for enemy in to_load:
            
            try:
                if enemy["sub"]=="boss":
                    Enemy(self,boss.x,boss.y,type,level)
                    
                  
                elif enemy["sub"]=="miniboss":
                    Enemy(self,miniboss.x,miniboss.y,type,level)
                    
            except:
                   while enemy["amount"]>0:  #and enemy["sub"]=="usual":               
                    enemy["amount"]-=1
                    spread=random.randint(-100,100)
                   
                    pos=vec(pos_X+spread,pos_Y)
                    type=enemy["type"]
                    level=enemy["level"]
                    Enemy(self,pos.x,pos.y,type,level)
           
          
               

                
                
                
      
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):

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

        self.screen.blit(text_surface, text_rect)


    def run(self):

        # игровой цикл если False => вырубить


        while self.running:

            self.dt = self.clock.tick(FPS) /1000

            self.events()

            self.update()

            self.draw()
        


    def quit(self):

        pg.quit()

        sys.exit()



    def update(self):
       
        # обновление кадра
        
             
           if not self.player_1.inv.active and not self.player_1.stats.active:
             
                  self.all_sprites.update()

                  self.camera.update(self.current_actor)
             
           else:
               self.HUD_components.update()
           if len(self.heroes)==0:
               for mob in self.enemies:
                      mob.necrologue()
               self.write_necrologue()
                     
               self.running=False
           if self.mode=="infinity":
              if len(self.enemies)==0:
                  self.write_necrologue()
                  self.running=False

                      
        
              
               
               

    def draw_grid(self):

        for x in range(0, WIDTH, TILESIZE):

            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):

            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))



       
       
    
    def draw(self):
       self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))
           #hud              
       if HUD.check_for_draw(self.player_1):        
        for sprite in self.all_sprites:           
             self.screen.blit(sprite.image,self.camera.apply(sprite))
        HUD.draw_bar(self)
       else:
            HUD.draw_in_scene(self)
            HUD.draw_HUD_of_players(self)

       self.draw_text(str(int(self.clock.get_fps())),READABLE_FONT,30,RED,960,50)
     

       pg.display.flip()

    def events(self):

       

        for event in pg.event.get():
            if event.type == pg.QUIT:

                self.quit()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    self.quit()
            
                    #именованые первого
            if event.type==pg.KEYDOWN:
                 controlling(event,self.player_1)
                 
            if event.type==pg.MOUSEBUTTONDOWN:    #отклик мыши
               
                for hero in self.heroes:
                    if hero.inv.active:
                       hero.inv.interaction(event.button)
                       
                    if hero.stats.active:
                       hero.stats.interaction(event.button)



           

    

class Controller():
    def __init__(self):
        try:
            with open("files\\data\\level.json") as file:
                 data=json.load(file)
            self.last_level=data["level"]
            
        except:
              self.last_level=0
      
        language_manager.load_controller() 
        self.interest_state=0
        self.health_state=0
        self.progress_state=0
        self.decision=0
        self.mode="challenge"
        self.story_maps=LEVELS
        self.infinity_maps=[fire_level,ice_level]
        self.music=True
        self.DJ=music_manager.DJ()
        self.packs=[[{"type":"jumper","amount":20}],[{"type":"ninja","amount":10},{"type":"passive","amount":10},{"type":"canon","amount":10}],
                    [ {"type":"ninja","amount":1,"sub":"boss"}],[{"type":"ninja","amount":1,"sub":"miniboss"},{"type":"passive","amount":10}],[{"type":"ninja","amount":10}],[{"type":"passive","amount":20}]]
        
        
      
            
   
    def game_loop(self,game):
        game.new()
        while game.running:
            game.run()
    def create_random_squad(self,n):

        exceptions=["boss","miniboss"]
        pack=random.choice(self.packs)
        
        for set in pack:
            for enemy in pack:
                try:
                    if enemy["sub"]=="boss":
                         enemy["level"]=n*10+5
                    elif enemy["sub"]=="miniboss":
                      enemy["level"]=n*5+5
                except:
                    enemy["sub"]="usual"
                    enemy['level']=40*n/set['amount']              
        return pack
    def analyze(self):
          self.last_level+=1
          #analysis.update()
         
          for hero in self.cur_game.heroes:
              hero.wave=self.last_level
              hero.save_data()
        

              
          

         
  
    def print_wave(self):
        
       if self.mode=="challenge":
            print("******************************************************** WAVE "+str(self.last_level)+"********************************************************")
       elif self.mode=="story":
           print("********************************************************CHAPTER "+str(self.last_level)+"*******************************************************")

    def launch_new_game(self):
          try:
              self.cur_game.running=False
          except:
              pass
          if self.mode=="story":         
              if self.last_level==0:
                  self.delete_saving()           
              self.cur_game=Game(self.story_maps[self.last_level],self.DJ,self.last_level,mode="story")
          elif self.mode=="challenge":            
                 pack=self.create_random_squad(self.last_level)
                 map=random.choice(self.infinity_maps)
                 print(map)
                 self.cur_game=Game(random.choice(self.infinity_maps),self.DJ,self.last_level,pack)

                 self.cur_game.DJ.play_random_infinity()
          self.cur_game.new()
          self.print_wave()
          with open("files\\data\\level.json",'w') as file:
              json.dump({"level":self.last_level},file)
          
    def delete_saving(self):
        try:

            os.unlink(saving_file)
        except:
            print("no saved game found")
        try:
            os.unlink("files\\data\\level.json")
        except:
            pass
    def comand(self):
         
          while True:
            a=input("Command : ")
            if a=="zeta":
                self.mode="story"
                print("current mode "+self.mode)
                
            elif a=="infinity":
                self.mode="challenge"
                print("current mode "+self.mode)
            elif a=="ok":
                break
            elif a=="set wave":
                self.last_level=int(input())
            elif a=="music off":            
                self.DJ.off()
            elif a=="music on":        
                self.DJ.on()
            elif a=="music on":        
                self.DJ.on()
            
               
            #elif a=="hero set level":        
            #    b=input("Name")
            #    if b!="all":
            #        for hero in self.cur_game.heroes:
            #            if hero.nick_name==b:
            #                c=int(input("set level :"))
            #                hero.level=c
            #            else:
            #                print("incorrect")
            #    else:
            #        c=int(input("set level :"))
                           
            #        for hero in self.cur_game.heroes:
            #             hero.level=c
            



    def protocol(self):
        self.comand()
        self.launch_new_game()
       
        while True:
            if  not self.cur_game.running: 
              if len(self.cur_game.heroes)>0:
                self.analyze()
                self.launch_new_game()
              else:
                  if self.mode!="story":
                    self.delete_saving()
                    
                  print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DEAD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                  break
            if len(self.cur_game.enemies)==0 and self.mode=="challenge":
                
                 self.analyze()
                 self.launch_new_game()
            self.game_loop(self.cur_game)
       

c=Controller()

c.protocol()

