import pygame as py
from settings import *
import pytmx
class Map:
    def __init__(self,filename):
        self.data=[]
        with open(filename,'rt') as file:
         for line in file:
            self.data.append(line.strip())
        self.tilewidth=len(self.data[0])
        self.tileheight=len(self.data)
        self.width=self.tilewidth*TILESIZE
        self.height=self.tileheight*TILESIZE



class Tilemap:
    def __init__(self,filename):
        self.filename=filename
        tm=pytmx.load_pygame(filename,pixelalpha=True)
        self.width=tm.width*tm.tilewidth
        self.height=tm.height*tm.tileheight
        self.tmxdata=tm
    def render(self,surface):
        ti=self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if self.filename.endswith(level_1):
                            
                            what=32
            else:
                            what=0
            if isinstance(layer,pytmx.TiledTileLayer):
                for x,y,gid in layer:
                    tile=ti(gid)
                    if tile:
                        
                        surface.blit(tile,(x*self.tmxdata.tilewidth,y*self.tmxdata.tileheight-what))
    def make_map(self):
        temp_surface=py.Surface((self.width,self.height))
        self.render(temp_surface)
        return temp_surface
class Camera:
    def __init__(self,width,height):
        self.camera=py.Rect(0,0,width,height)
        self.width=width
        self.height=height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)
    def apply_rect(self,rect):
        return rect.move(self.camera.topleft)
    def update(self,target):

        x=-target.rect.x + int(WIDTH/2)
        
        y=-target.rect.y+int(HEIGHT/2)
        #ограничение листания карты
        x=min(0,x) #левый край
        y=min(0,y) #верхний
        x=max(-(self.width-WIDTH),x)
        y=max(-(self.height-HEIGHT),y)
        self.camera=py.Rect(x,y,self.width,self.height)
       