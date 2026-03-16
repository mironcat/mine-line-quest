import math
import time
import random
class Character:
    """Класс для представления персонажа"""
    def __init__(self, filename, x, y, clear_backgound = True):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                template = file.read().split('\n')
        except FileNotFoundError:
            print(f"Файл {filename} не найден!")
            template = []  # или другое значение по умолчанию
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
        self.template = template
        self.height = len(template)
        self.width = len(template[0]) if template else 0
        self.x = x
        self.y = y
        self.clear_backgound = clear_backgound

    def update_background(self, filename, clear_backgound = True):
        """Обновляет изображение персонажа из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.template = f.read().splitlines()
                self.height = len(self.template)
                self.width = len(self.template[0]) if self.template else 0                
                self.clear_backgound = clear_backgound
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
    def move_right(self,speed:int):
        self.x+=speed
    def move_left(self,speed):
        self.x-=speed
    def get_char(self, row, col):
        # Возвращает символ в указанной позиции 
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.template[row][col]
        return ' '

class Event:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Message():
    def __init__(self):
        self.template = [
            '---------------------------',
            '|           Hello!        |',
            '---------------------------'
        ]
        self.height = len(self.template)
        self.width = len(self.template[0]) if self.template else 0
        self.x = 1
        self.y = 1
    
    def get_char(self, row, col):
        # Возвращает символ в указанной позиции
        if 0 <= row < self.height and 0 <= col < self.width:
            # Проверяем, не выходит ли col за длину конкретной строки
            if col < len(self.template[row]):
                return self.template[row][col]
            return ' '  # Если col больше длины строки, возвращаем пробел
        return ' '


class Inventory(Message):
    def __init__(self):
        super().__init__()  # Вызов конструктора родителя
        self.wood = 0
        self.stones = 0
        self.iron = 0
        self.clear_backgound=True
        self.resources = ['wood', 'stones', 'iron']  # список ресурсов
        self.update()
    
    def update(self):
        w = str(self.wood)      # Преобразуем в строку
        s = str(self.stones)    # Преобразуем в строку
        i = str(self.iron)      # Преобразуем в строку
        
        self.template = [
            '|--------------------|',
            f'| ДЕРЕВО: {w:<7}    |',
            f'| ЖЕЛЕЗО: {i:<7}    |',
            f'| КАМНИ:  {s:<7}    |',
            '|--------------------|'
        ]
        
        # Обновляем размеры
        self.height = len(self.template)
        # Находим максимальную длину строки в template
        self.width = max(len(line) for line in self.template) if self.template else 0
    
    def collect_resource(self, resource_name: str, amount: int) -> None:
        if resource_name in self.resources:
            current_value = getattr(self, resource_name)
            setattr(self, resource_name, current_value + amount)
            self.update()
        else:
            print(f"Ресурс '{resource_name}' не существует!")
            input("Нажмите любую клавишу")


class Man (Character):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.event = Event('newborn', '')
        self.money = 200-100
        self.active_character = None
        self.inventory = Inventory()
        self.supporter = None
        self.name = 'Вадик'
        self.command = ''
    def reset_event(self):
        self.event = Event('пусто', '')
    def set_event(self, event):
        self.event = event
    def set_active_character(self, character):
        self.active_character = character
    def interaction(self, ):
        self.active_character.on_action(self)

class NPC (Character):
    
    def __init__(self, filename, x, y, clear_backgound = True):
        super().__init__(filename, x, y, clear_backgound)
        self.critic_distance = 3
        self.age = 0
        self.showOnLevel = True
        self.stopMan = False
    def check_critic_distance(self, man):
        # Вычисляем евклидово расстояние между деревом и человеком
        distance = math.sqrt((self.x - man.x)**2 + (self.y - man.y)**2)
        # отображение дистанции
        print(f"{self.__class__.__name__}:{distance}")
        return distance <= self.critic_distance

class Lodka (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.critic_distance = 6
        self.stopMan = True
    def each_tick (self):
        self.age+=1
        pass
    def near_event_message(self):
        return "вы можете сесть в лодку"
    def near_man(self, man):
        if self.stopMan: man.x = self.x-6
        pass
    def on_action(self, man):
        # это происходит когда нажато e
        self.showOnLevel=False
        self.stopMan=False
        self.critic_distance =-1
        # превращаюсь в сидящего в лодке чувака
        man.x = self.x+2 # перемещаюсь чтобы сесть в лодку
        man.update_background('heroes/manlodka.txt')
        man.set_event(Event('next_screen', '9'))
        pass

class Wall (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y, clear_backgound=False)  # Вызов конструктора родителя
        self.critic_distance = 6
        self.stopMan = True
    def each_tick (self):
        self.age+=1
        pass
    def near_event_message(self):
        return "нет прохода"
    def near_man(self, man):
        if self.stopMan and man.command == "a": man.x = self.x+6
        if self.stopMan and man.command == "d": man.x = self.x-6
        pass
    def on_action(self, man):
        pass

class Javal (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.resource = 2
        self.critic_distance = 4
        self.stopMan = True
    def each_tick (self):
        # это выполняется каждый шаг(ход) man'а на текущем уровню
        self.age+=1
        pass
    def near_event_message(self):
        # это сообщение показывается когда critic_distance<=расстоянию до man
        return "⛏️"
    def near_man(self, man):
        if self.stopMan: man.x = self.x-6
        # это происходит когда critic_distance<=расстоянию до man
        #print ('Hello Man!')
        pass
    def on_action(self, man):
        # это происходит когда нажато e
        self.showOnLevel=False
        self.stopMan=False
        self.critic_distance =-1
        man.inventory.collect_resource('stones',self.resource)
        self.resource = 0
class Tree (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.resource = 2
        self.critic_distance = 4
    def each_tick (self):
        self.age+=1
        pass
    def near_event_message(self):
        return "🌲"
    def near_man(self, man):
        #print ('Hello Man!')
        pass
    def on_action(self, man):
        # Ай!
        self.update_background('heroes/brocken_tree.txt')
        man.inventory.collect_resource('wood',self.resource)
        self.resource = 0
class Ore (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.resource = random.randrange(2, 6)
        self.critic_distance = 5
    def each_tick (self):
        self.age+=1
        pass
    def near_event_message(self):
        if self.resource != 0: return "⛏"
        else:
            return" "
    def near_man(self, man):
        return 'Hello Man!'
        pass
    def on_action(self, man):
        self.showOnLevel = False
        if self.resource != 0:
            man.inventory.collect_resource('iron', self.resource)
            man.inventory.collect_resource('stones', random.randrange(0, 4))
            self.resource = 0
class Dragon (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.critic_distance = 4
    def each_tick (self):
        self.age+=1
        #print ('Ухх..')
        pass
    def near_event_message(self):
        return "💭"
    def near_man(self, man):
        print (f'Джек: Привет {man.name}!')
        pass
    def on_action(self, man):
        # Ай!
        print (f'{man.name}: Привет Дракон Джек! Хочешь пойти со мной?')
        time.sleep(1)
        print (f'Джек: ...')
        time.sleep(1)
        print (f'Джек: Да, хочу!')
        if input(f"{man.name}: Принять в команду? (y/n)") == 'y':
            self.showOnLevel=False
            man.supporter = self
            print (f'Джек принят в команду')
            input('нажмите любую клавишу') 
            
        else:
            print (f'Джек: Пока!')
            input('нажмите любую клавишу')
        pass