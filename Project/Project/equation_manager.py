
import random
import json
import time
from settings import *
def soroban(level):
        if level=='easy':
            rounds=10
            diap=(-5,5)
            sleep_time=1.5
        elif level=='medium':
            rounds=15
            diap=(-10,10)
            sleep_time=3
        elif level=='hard':
            rounds=20
            diap=(-50,50)
            sleep_time=4
        print("Starting!")
        i=1
        sum=0
        while i<rounds:
                a=random.randint(diap[0],diap[1])
                if a==0:
                    a=2
                if a>0:
                   print("+"+str(a))
                else:
                 print(str(a))
                sum+=a
                time.sleep(sleep_time)
                i+=1
        try:
          a=int(input("Enter your answer: "))
        except:
            print("You need to enter number")
        if a==sum:
               return True
        else:
            return False
def printer(filename):
    with open(filename) as file:
            data=json.load(file)
    temp=data[random.randint(0,len(data)-1)]
    print(temp['equation'])
    print("Possible answers:")
    for key,value in temp.items():
        if key!='equation' and key!='correct':
            print(key+" : "+value)
    a=input("Your answer is : ").lower()
    a=a.strip()
    if a==temp['correct']:
        return True
    else:
        return False

def equation(player):
    if player.spec=='warrior':
        if printer(warrior_file):
            return True
    elif player.spec=='wizard':
        if printer(wizard_file):
            return True

    elif player.spec=='archer':
        if soroban('easy'):
            return True
    elif player.spec=='priest':
        if printer(warrior_file):
            return True
    else:
        return False