# создатель exe файла
# pyinstaller --clean .\make_exe.spec   
import copy
from modules.main import ASCIIArt
from modules.characters import Man
import os
#os.system('mode con: cols=180 lines=30')
import time
# import keyboard  # pip install keyboard

clear = lambda: os.system('cls')


man = Man('heroes/man.txt', x=5,y=3)
man.name = input('Представьтесь, пожалуйста: ')
#man.name = 'Вадик'
man.command=""
current_level = ASCIIArt()
answer:str = ""
input_str:str = ""
screen_name:str = "1"
last_screen_name = screen_name
last_answer=""
intro = current_level.load_scene("0")
current_level.display(intro, underground=False)
input('Нажмите любую клавишу чтобы начать игру.')
clear()
full_scene = current_level.load_scene(screen_name)
game_state = {}
man_action=""

while answer != "q":
        last_screen_name = screen_name
        if man.event.type=='next_screen' or man.event.type=='newborn':
            if screen_name in game_state:
                # Восстанавливаем из сохранения
                current_level = game_state[screen_name]
                full_scene = current_level.draw_scene_characters()
            else: 
                full_scene = current_level.load_scene(screen_name)
                #print(current_level.characters)
            man.x=current_level.man_init_x
            man.y=current_level.man_init_y
        
        scene = current_level.draw_man(man, full_scene)
        # scene = current_level.draw_character(dragon)
        #-----------------------------------------
        #time.sleep(.1)
        clear()
        # показываем инвентарь, если нужно
        if (answer == 'i'):
            scene = current_level.show_inventory(man,scene)    
        
        current_level.update_characters(man)
        if man.event.type=='near_event': man_action = man.event.value
        print(f"a - влево, d - вправо, i- инвентарь, e - взаимодействие (можно сделать):{man_action}")
        print(f"уровень:{screen_name} деньги: {man.money}")    

        current_level.display(scene, underground=False)
        # Рисуем реакцию персонажей
        man_action=""
        if man.event.type=='near_event': man.active_character.near_man(man)
        if input_str == "" : 
             input_str = input(f"{man.name}: ")
        if input_str == "" : 
             answer = "" 
             input_str = ""  # остаток строки
        else: 
             answer = input_str[0]
             input_str = input_str[1:]  # остаток строки
        man.command=answer
        last_answer = answer
        #------------------------------------------
        
        if ((answer == 'd' or answer == 'в')):
            man.move_right(speed=3)
        if ((answer =='a' or answer == 'ф' )):
            man.move_left(speed=3)
        if man.event.type=='near_event' and answer == 'e':
            man.interaction()
            full_scene = current_level.draw_scene_characters()
            #full_scene = current_level._draw_character_on_scene(full_scene, man.active_character)
        
        if man.event.type=='next_screen':
                game_state[last_screen_name] = copy.deepcopy(current_level) # сохраняем старое состояние 
                screen_name = man.event.value
        

