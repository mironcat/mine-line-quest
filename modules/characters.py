import math
class Character:
    """Класс для представления персонажа"""
    def __init__(self, filename, x, y):
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

    def update_background(self, filename):
        """Обновляет изображение персонажа из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.template = f.read().splitlines()
                self.height = len(self.template)
                self.width = len(self.template[0]) if self.template else 0                
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
class Inventory (Character):
    def __init__(self):
        self.resources = {
            'wood': 0,
            'stones': 0,
            'glass': 0
        }
    def update_template(self):
        wood = self.resources.wood
        stones = self.resources.stones
        iron = self.resources.iron
        diamods = self.resources.diamods
        self.template = [
        '--------------------',
        '| ДЕРЕВО:'+wood+'          |',
        '| ЖЕЛЕЗО:'+iron+'         |',
        '| АЛМАЗЫ:'+diamods+'         |',
        '| КАМНИ:'+stones+'          |',
        '--------------------'
        ]
    def collect_resource(self, resource: str, amount: int) -> None:
        if resource in self.resources:
            self.resources[resource] += amount
            self.update_template()
        else:
            print(f"Ресурс '{resource}' не существует!")
    
    def __getattr__(self, name):
        #Позволяет обращаться к ресурсам как к атрибутам
        if name in self.resources:
            return self.resources[name]
        raise AttributeError(f"'Inventory' object has no attribute '{name}'")

class Man (Character):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.event = Event('newborn', '')
        self.money = 100
        self.active_character = None
    def show_inventory(self):
        self.inventory.show()
    def set_event(self, event):
        self.event = event
    def set_active_character(self, character):
        self.active_character = character
    def interaction(self):
        self.active_character.on_action(self)

class NPC (Character):
    
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)
        self.critic_distance = 3
        self.age = 0
    def check_critic_distance(self, man):
        # Вычисляем евклидово расстояние между деревом и человеком
        distance = math.sqrt((self.x - man.x)**2 + (self.y - man.y)**2)
        return distance <= self.critic_distance

class Tree (NPC):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)  # Вызов конструктора родителя
        self.resource = 2
        self.critic_distance = 4
    def each_tick (self):
        pass
    def near_event_message(self):
        return "🌲"
    def near_man(self):
        print ('Hello Man!')
    def on_action(self, man):
        # Ай!
        self.update_background('heroes/brocken_tree.txt')
        man.inventory.collect_resource('wood',self.resource)
        self.resource = 0