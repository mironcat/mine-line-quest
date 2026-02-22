from modules.characters import *
class ASCIIArt:
    def __init__(self, background_art=None):
        #   background_art (list): изображение
        self.background = background_art if background_art else []
        self.characters = []
        self.man_init_x = 0
        self.man_init_y = 0
        

    def load_scene(self,screen_name):
         screen_filename ='screens/'+screen_name+'.txt'
         self.set_background(screen_filename)
         return self.draw_scene_characters(clear_area=True)
    
    def set_background(self, filename):
        """Загружает изображение из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.background = f.read().splitlines()
                self.characters = self.add_characters()  # это создает персонажей
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
    
    def add_characters(self):
        """Создает персонажей на основе последних строк фона"""
        # Проверяем, что в фоне есть хотя бы 2 строки
        if len(self.background) < 2:
            print("Недостаточно строк в фоне для создания персонажей")
            return []
            
        under_types = self.background[-3]  # строка с типами
        under_coords2 = self.background[-2]  # строка с Y-координатами
        under_coords1 = self.background[-1]  # строка с Y-координатами
        self.characters = []
        
        # Проверяем, что координатная строка не короче строки с типами
        min_length = min(len(under_types), len(under_coords1))
        
        for index in range(min_length):
            symbol = under_types[index]
            try:
                # Преобразуем символ координаты в число
                y = self.get_coords(under_coords1,under_coords2, index)
            except (ValueError, IndexError):
                y = 0  # значение по умолчанию
            if symbol == '@':
                self.man_init_x=index-2
                self.man_init_y=y
            elif symbol == 't':
                tree = Tree(filename='heroes/tree.txt', x=index-2, y=y)
                self.characters.append(tree)
            elif symbol == 'd':
                dragon = Dragon(filename='heroes/dragon.txt', x=index-2, y=y)
                self.characters.append(dragon)
            elif symbol == 'm':
                mine = Tree(filename='heroes/mine.txt', x=index-2, y=y)
                self.characters.append(mine)
            # Можно добавить другие типы
            # elif symbol == 'g':
            #     goblin = Character('heroes/goblin.txt', x=index, y=y)
            #     self.characters.append(goblin)
                
        return self.characters
    def get_coords(self, under_coords1,under_coords2, index):
            # Разбиваем строки на отдельные символы
        coord_str = under_coords1[index]+under_coords2[index]
        return int(coord_str)
    
    def create_character(self, template):
        """
        Создает персонажа из шаблона
        Args:
            template (list): список строк с шаблоном персонажа
        """
        return Character(template)
    
    def draw_scene_characters(self, clear_area=True):
        """Рисует персонажей на сцене"""
        if not self.background:
            print("Нет фонового изображения")
            return None
            
        # Начинаем с копии фона
        scene = self.background.copy()
        
        # Рисуем каждого персонажа
        for character in self.characters:
            # Рисуем персонажа на сцене
            scene = self._draw_character_on_scene(scene, character, clear_area)
        
        return scene
    
    def _draw_character_on_scene(self, scene, character, clear_area=True):
        """Вспомогательный метод для отрисовки одного персонажа на сцене"""
        # Создаем копию сцены для работы
        result_scene = scene.copy()
        
        # Если нужно, очищаем область
        if clear_area:
            result_scene = self._clear_area(result_scene, character.x, character.y, 
                                           character.width, character.height)
        
        # Рисуем персонажа
        for i in range(character.height):
            if character.y + i >= len(result_scene):
                break
            line = list(result_scene[character.y + i])
            for j in range(character.width):
                if character.x + j < len(line):
                    char = character.get_char(i, j)
                    if char != ' ':  # не заменяем пробелы
                        line[character.x + j] = char
            result_scene[character.y + i] = ''.join(line)
            
        return result_scene
    def show_inventory(self, man, scene):
     
     return self._draw_character_on_scene(scene, man.inventory)
        
    def draw_man(self, character, scene, clear_area=True):
        """
        Рисует основно персонажа на фоне
        
        Args:
            character: объект Character
            clear_area (bool): очищать ли область перед отрисовкой
            add_to_background (bool): обновлять ли background
        """
        
        # Рисуем персонажа на сцене
        scene = self._draw_character_on_scene(scene, character, clear_area)
        
        # ----- Смотрим что под ногами-------
        under_types = scene[-3]  # строка с типами
        under_foot= under_types[character.x]
        try:
            int(under_foot)
            character.set_event(Event('next_screen', under_foot))
        except (ValueError, TypeError):
                if under_foot == '!':
                    event = Event('нет прохода', under_foot)
                elif under_foot == ' ':
                    event = Event('пусто', under_foot)
                else: 
                    event = Event('другое', under_foot)
                character.set_event(event)
        # -----------------------------------
        return scene
    
    def _clear_area(self, scene, x, y, width, height):
        """Очищает область для отрисовки"""
        result_scene = scene.copy()
        for i in range(height):
            if y + i < len(result_scene):
                line = list(result_scene[y + i])
                for j in range(width):
                    if x + j < len(line):
                        line[x + j] = ' '
                result_scene[y + i] = ''.join(line)
        return result_scene
    
    def display(self, scene: list, underground: bool = False) -> None:
        """Отображает сцену. Если underground=True, показывает последнюю строку."""
        if underground:
            screen = scene
        else:
            screen = scene[:-3] if len(scene) > 2 else scene
            
        for line in screen:
            print(line)
    
    def update_characters(self, man):
        """Обновляет  персонажей (например, для анимации)"""
        
        for character in self.characters:
            # рассчитываем расстояние до персонажа     
            if (character.check_critic_distance(man) == True):
                character.near_man(man)
                man.set_event(Event('near_event', character.near_event_message()))
                man.set_active_character(character)                

        # Здесь можно добавить логику движения персонажей
        pass


    


