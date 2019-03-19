# цвета в RGB
import pygame as pg
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# настройки игры 
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Testing in progress"
BGCOLOR = (122,122,122)



TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
GRAVITY=0.8
MOB_FRICTION=-0.12
#настройки персонажа
PLAYER_SPEED=300
basic_file='files\\data\\basic.json'
warrior_file='files\\data\\equations\\warrior_equations.json'
wizard_file='files\\data\\equations\\wizard_equations.json'
priest_file='files\\data\\equations\\priest_equations.json'
enemies_file='files\\data\\enemy.json'
boss_file="files\\data\\bosses.json"
items_file='files\\data\\items.json'
saving_file='files\\data\\data.json'

languages_folder='files\\languages\\'

#изображения игрока
warrior_sprite_list="img\\heroes\\warrior_spritelist.png"
wizard_sprite_list="img\\heroes\\wizard_spritelist.png"
archer_sprite_list="img\\heroes\\archer_spritelist.png"
priest_sprite_list="img\\heroes\\priest_spritelist.png"
wizard_image_file='img\\heroes\\mage_solo.png'
archer_image_file='img\\heroes\\archer_solo.png'
priest_image_file='img\\heroes\\priest_solo.png'

HUD_inventory_file='img\\HUD\\inventory.png'
STATS_FILE='img\\HUD\\stats.png'
HUD_hint_file='img\\HUD\\hint.png'
HUD_main_menu_file='img\\HUD\\menu.png'
DESCRIPTION_FOLDER='\\ability_description\\'
PLOT_FOLDER='files\\data\\plots\\'
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)
FONT_FILE_ENG="files\\fonts\\IMMORTAL.ttf"
FONT_FILE_RUS="files\\fonts\\rus_font.ttf"
SUB_FONT_FILE="files\\fonts\\Algerian.ttf"
READABLE_FONT="Files\\fonts\\pixeled.ttf"

#врага
canon_image='img\\enemies\\canon.png'

img_leveler='img\\objects\\leveler.png'
bars_metal='img\\objects\\bars.png'
bars_spikes='img\\objects\\b_spikes.png'

#ловушки
saw_image='img\\enemies\\saw.png'
spike_image='img\\objects\\spikes.png'

ICON_FOLDER="img\\icons\\"
ANALYSIS_FOLDER="files\\data\\analysis\\"

#уровни
test_level='test_level.tmx'
level_1='level_1.tmx'
level_2='level_2.tmx'
level_3='level_3.tmx'
LEVELS=[level_1,level_2,level_3]

fire_level="fire_level.tmx"
ice_level="ice_level.tmx"

