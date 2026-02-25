import copy

from modules.main import ASCIIArt
from modules.characters import Man
import os
import time
# import keyboard  # pip install keyboard

clear = lambda: os.system('cls')


man = Man('heroes/man.txt', x=5,y=3)
#man.name = input('ваше имя')
man.name = 'Вадик'
current_level = ASCIIArt()
answer:str = ""
input_str:str = "start"
screen_name:str = "1"
last_screen_name = screen_name
#last_answer=""
# intro = current_level.load_scene("0")
# current_level.display(intro, underground=False)
# input('Нажмите любую клавишу чтобы начать игру.')
#clear()
full_scene = current_level.load_scene(screen_name)
game_state = {}
man_action=""

while answer != "q":
    if input_str=="start": input_str = "e"
    else:  input_str = input(f"{man.name}: ")
    if "q" in input_str: input_str = "q"
    
    for answer in input_str:
        last_answer = answer
        last_screen_name = screen_name
        if man.event.type=='next_screen' or man.event.type=='newborn':
            if screen_name in game_state:
                # Восстанавливаем из сохранения
                current_level = game_state[screen_name]
                full_scene = current_level.draw_scene_characters(clear_area=True)
                
            else: 
                full_scene = current_level.load_scene(screen_name)
                #print(current_level.characters)
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
        print(f"уровень:{screen_name} деньги: {man.money}")    

        current_level.display(scene, underground=False)
        # Рисуем реакцию персонажей
        
        #print("Messages:")
        #man.reset_event()
        man_action=""
        if man.event.type=='near_event': man.active_character.near_man(man)
    
        #------------------------------------------
        
        if (answer == 'd' or answer == 'в' ):
            man.move_right(speed=3)
        if (answer =='a' or answer == 'ф' ):
            man.move_left(speed=3)
        
        if man.event.type=='near_event' and answer == 'e':
            man.interaction()
            full_scene = current_level.draw_scene_characters(clear_area=True)
            #full_scene = current_level._draw_character_on_scene(full_scene, man.active_character)
        
        
        
        if man.event.type=='next_screen':
                game_state[last_screen_name] = copy.deepcopy(current_level) # сохраняем старое состояние 
                screen_name = man.event.value
        

