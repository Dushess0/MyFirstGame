import json as js
file="logs\\mob_efficiency.json"

w1=0.05
w2=0.12

def finding_k(dictionary):

    
    if dictionary["last hit"]:
        last_hit=1
    else:
        last_hit=0

    k=dictionary['time survived']*w1+dictionary["dealed damage"]*w2+last_hit
    
    return k
def make_average(type,all_files):
    list_of_type=[]
    
    for file in all_files:
        if file["type"]==type:
            list_of_type.append(file)

    average_k=0
    average_damage=0
    average_lifetime=0
    total_kills=0
    total_deaths=0
    i=0
    for mob in list_of_type:
        i+=1
        average_k+=finding_k(mob)
        average_damage=+mob["dealed damage"]
        average_lifetime+=mob['time survived']
        if mob['last hit']:
         total_kills+=1
        if not mob['survived']:
         total_deaths+=1
   
    average_k=round((average_k/i),2)
    average_damage=round((average_damage/i),2)
   
    average_lifetime=round((average_lifetime/i),2)
    dictionary={"type":type,"average lifetime":average_lifetime,
                "average damage":average_damage,"average k":average_k,
                "total kills":total_kills,"total deaths":total_deaths}
   
    
    with open("AI\\mobs_balance.json") as file_obj:
        data=js.load(file_obj)
    data.append(dictionary)
    print(data)
    with open("AI\\mobs_balance.json",'w') as file_obj:
        js.dump(data,file_obj)



def update() : 

    list=[]
    with open("AI\\mobs_balance.json",'w') as file_obj:
            js.dump(list,file_obj)

    with open("logs\\mob_efficiency.json") as file_obj:
        all_files=js.load(file_obj)
        
    unique_types=[]
    for file in all_files:
        if file["type"] not in unique_types:
            unique_types.append(file['type'])
    for type in unique_types:
        make_average(type,all_files)


update()


