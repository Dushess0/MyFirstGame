import json as js


def make_average_class(clas,all_files):
    list_of_classes=[]
    
    for file in all_files:
        if file["Class"]==clas:
            list_of_classes.append(file)

    
    average_damage=0
    average_level=0
    average_kills=0
    average_wave=0
    i=0
    max_damage=0
    max_wave=0
    max_level=0
    max_kills=0
    for mob in list_of_classes:
        i+=1
        average_damage=+mob["Dealed damage"]
        average_level+=mob['Level']
        average_kills+=mob["mobs killed"]
        average_wave+=mob["wave"]

        max_damage=max(max_damage,mob["Dealed damage"])
        max_wave=max(max_wave,mob["wave"])
        max_level=max(max_level,mob["Level"])
        max_kills=max(max_level,mob["mobs killed"])


    average_level=round((average_level/i),2)
    average_damage=round((average_damage/i),2)
    average_kills=round((average_kills/i),2)
    average_wave=round((average_wave/i),2)
    dictionary={"Class":clas,"max kills":max_kills,
                "max damage":max_damage,"max level":max_level,
                "max wave":max_wave,"average kills":average_kills,
                "average damage":average_damage,"average level":average_level,"average wave":average_wave}
    
    with open("rank\\class_ranked.json",) as file_obj:
        list=js.load(file_obj)
    list.append(dictionary)
    with open("rank\\class_ranked.json",'w') as file_obj:
        js.dump(list,file_obj)


        
def make_average_personal(name,all_files):
    list_of_classes=[]
    
    for file in all_files:
        if file["Name"]==name:
            list_of_classes.append(file)

    
    average_damage=0
    average_level=0
    average_kills=0
    average_wave=0
    i=0
    max_damage=0
    max_wave=0
    max_level=0
    max_kills=0
    for mob in list_of_classes:
        i+=1
        average_damage=+mob["Dealed damage"]
        average_level+=mob['Level']
        average_kills+=mob["mobs killed"]
        average_wave+=mob["wave"]

        max_damage=max(max_damage,mob["Dealed damage"])
        max_wave=max(max_wave,mob["wave"])
        max_level=max(max_level,mob["Level"])
        max_kills=max(max_level,mob["mobs killed"])


    average_level=round((average_level/i),2)
    average_damage=round((average_damage/i),2)
    average_kills=round((average_kills/i),2)
    average_wave=round((average_wave/i),2)
    dictionary={"Name":name,"max kills":max_kills,
                "max damage":max_damage,"max level":max_level,
                "max wave":max_wave,"average kills":average_kills,
                "average damage":average_damage,"average level":average_level,"average wave":average_wave}
    
    with open("rank\\user_ranked.json",) as file_obj:
        list=js.load(file_obj)
    list.append(dictionary)
    with open("rank\\user_ranked.json",'w') as file_obj:
        js.dump(list,file_obj)





def update_classes() : 

    list=[]
    with open("rank\\class_ranked.json",'w') as file_obj:
            js.dump(list,file_obj)

    with open("logs\\level_result.json") as file_obj:
        all_files=js.load(file_obj)
        
    unique_classes=[]
    for file in all_files:
        if file["Class"] not in unique_classes:
            unique_classes.append(file['Class'])

    for spec in unique_classes:
        make_average_class(spec,all_files)

def update_personal():
    list=[]
    with open("rank\\user_ranked.json",'w') as file_obj:
            js.dump(list,file_obj)

    with open("logs\\level_result.json") as file_obj:
        all_files=js.load(file_obj)
        
    unique_names=[]
    for file in all_files:
        if file["Name"] not in unique_names:
            unique_names.append(file['Name'])

    for name in unique_names:
        make_average_personal(name,all_files)


update_classes()

update_personal()


