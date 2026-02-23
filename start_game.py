from modules.main import ASCIIArt
from modules.characters import Man
import os
#import time
# import keyboard  # pip install keyboard

clear = lambda: os.system('cls')


man = Man('heroes/man.txt', x=5,y=3)
#man.name = input('ваше имя')
man.name = 'Вадик'
current_level = ASCIIArt()
answer=""
screen_name = "0"
last_screen_name = ""
#last_answer=""
full_scene = current_level.load_scene(screen_name)
man_action=""
while answer != "q":
    
    if man.event.type=='next_screen' or man.event.type=='newborn':
            man.x=current_level.man_init_x
            man.y=current_level.man_init_y
    scene = current_level.draw_man(man, full_scene)
       # scene = current_level.draw_character(dragon)
    #-----------------------------------------

    clear()
    # показываем инвентарь, если нужно
    if (answer == 'i'):
        scene = current_level.show_inventory(man,scene)    
    
    current_level.update_characters(man)
    if man.event.type=='near_event': man_action = man.event.value
    print(f"a - влево, d - вправо, i- инвентарь, e - взаимодействие {man_action}")
    print(f"level:{screen_name} event:{man.event.type} деньги: {man.money}")    

    current_level.display(scene, underground=False)
    # Рисуем реакцию персонажей
    
    #print("Messages:")
    #man.reset_event()
    man_action=""
    if man.event.type=='near_event': man.active_character.near_man(man)
    answer = input(f"{man.name}: ")
    last_answer = answer
    #------------------------------------------
    
    if (answer == 'd' or answer == 'в' ):
        man.move_right(speed=3)
    if (answer =='a' or answer == 'ф' ):
        man.move_left(speed=3)

    if (answer == 'qi' and screen_name == "invent" ):
        screen_name = last_screen_name
        full_scene = current_level.load_scene(screen_name)
    if man.event.type=='next_screen':
        #next_scene = input('перейти на другую локацию? (n-отмена): ')
        #if next_scene!="n":
            screen_name = man.event.value
            full_scene = current_level.load_scene(screen_name)
  
    if man.event.type=='near_event' and answer == 'e':
         man.interaction()
         full_scene = current_level._draw_character_on_scene(full_scene,man.active_character)
    