import json
import os
from settings import languages_folder
import settings


def get_language():
    with open(os.path.join(languages_folder,"saved_language")+".json") as file_object:
                   data=json.load(file_object)
                   LANGUAGE=data['saved']
    return LANGUAGE

def get_font_from_language():
     try:
         with open(os.path.join(languages_folder,"saved_language")+".json") as file_object:
                       data=json.load(file_object)
                       LANGUAGE=data['saved']
         if LANGUAGE=="eng":
             FONT=settings.FONT_FILE_ENG
         elif LANGUAGE=='rus':
               FONT=settings.FONT_FILE_RUS
         elif LANGUAGE=='ukr':
              FONT=settings.FONT_FILE_ENG
         elif LANGUAGE=='pol':
              FONT=settings.FONT_FILE_ENG
         return FONT
     except:
         pass
   
def choosing_language():
    question=input("What language do you prefer?\n 1)ENGLISH\n 2)RUSSIAN\n 3)UKRAINIAN\n 4)POISH\n  ENTER : ")
    if question.startswith('1') or   question.lower()=='eng' or question.lower()=='engish'or question.lower().startswith('eng') :
            LANGUAGE="eng"
    elif question.startswith('2') or question.lower()=='rus' or  question.lower()=='russian'or question.lower().startswith('rus'):
            LANGUAGE="rus"
    elif question.startswith('3') or question.lower()=='ukr' or  question.lower()=='ukrainian' or question.lower()=='як реве дніпро' or question.lower()=='мова солов'+"'"+"їна" or question.lower()=='українська'or question.lower().startswith('uk') or question.lower().startswith('ук'):
            LANGUAGE="ukr"
    elif question.startswith('4') or question.lower()=='pol' or  question.lower()=='polish' or question.lower().startswith('pol'):
            LANGUAGE="pol"

    dict={"saved":LANGUAGE}

    with open(os.path.join(languages_folder,'saved_language.json'),'w') as file_obj:
        json.dump(dict,file_obj)

def load_controller():
    while True:
        try:

               with open(os.path.join(languages_folder,"saved_language")+".json") as file_object:
                   data=json.load(file_object)
                   LANGUAGE=data['saved']
                   break
        except:
             choosing_language()

    with open(os.path.join(languages_folder,"controller")+".json") as file_object:
           controller_data=json.load(file_object)
    return controller_data


def language_text(search):
        controller_data=load_controller()
        file=controller_data[search]
        with open(languages_folder+"\\"+get_language()+"\\"+file+".txt") as file:
            text=file.read()
        return text


