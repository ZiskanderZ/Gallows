#импорт необходимых библиотек
import pickle         #для сохранения в формат pkl
import sys            #для остановки игры
import time           #для преобразования в красивую дату
import os             #для очистки командной строки

def getGamerInput(is_level, is_one_two):                          #функция для ввода
    gamer_input = input()
    if gamer_input.lower() == 'stop':                   #если нужно остановить игру
        print('\nGoodbye')
        sys.exit(0)
    elif gamer_input.lower() == 'save' and (not is_level) and (not is_one_two): #если нужно сохранить
        return gamer_input
    elif len(gamer_input) == 1:
        if gamer_input.isdigit() and 1 <= int(gamer_input) <= 3:     #выбор в самом начале
            if is_level:
                return int(gamer_input)
            elif is_one_two and int(gamer_input) <= 2:    #выбор из двух ответов
                return int(gamer_input)
        elif (not is_level) and (not is_one_two) and gamer_input.isalpha():
            return gamer_input.lower()
    print('Error, try again')
    return getGamerInput(is_level, is_one_two)

def getNumber_save(folder):                                       #функция для полуения номера сохранения
    gamer_input = input()
    if gamer_input.isdigit():
        gamer_input = int(gamer_input)
        if 1 <= gamer_input <= len(os.listdir(folder)):            #меньше чем количество в папке файлов
            return gamer_input
    elif gamer_input.lower() == 'stop':
        print('Goodbye')
        sys.exit(0)
    print('Error, try again')
    return getNumber_save(folder)

class Slovo():                                                          # загаданное слово как класс
    def __init__(self, word, attemts_number, is_letter_in_word=False):
        self.word = word
        self.attemts_number = attemts_number
        self.is_letter_in_word = is_letter_in_word

        letter_list = [Letter(i, False) for i in word]
        self.letter_list = letter_list

        inputs_list = []
        self.inputs_list = inputs_list

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state['word'] = self.word
        state['attemts_number'] = self.attemts_number
        self.letter_list_dumps = pickle.dumps(self.letter_list)
        state['letter_list_dumps'] = self.letter_list_dumps
        state['inputs_list'] = self.inputs_list
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.word = state['word']
        self.attemts_number = state['attemts_number']
        self.letter_list_dumps = state['letter_list_dumps']
        self.letter_list = pickle.loads(self.letter_list_dumps)
        self.inputs_list = state['inputs_list']

    def check(self, input_letter):                        #проверка новой буквы в списке введенных букв
        if input_letter not in self.inputs_list:
            self.inputs_list.append(input_letter)
        else:
            print(f'You have already entered the letter "{input_letter}"')
            self.is_letter_in_word = True
        
    def decrease_attemts(self, input_letter):             #уменьшение колиства ходов
        if not self.is_letter_in_word:
            print(f'The letter "{input_letter}" is not in the word')
            self.attemts_number -=1

    def show(self, show_word_flag, input_letter=None):  #вовзращает открытое полностью слово 
        if show_word_flag:                              # или только с открытыми буквами
            new_word = self.word
            return new_word
        else:
            new_word = ''
            self.is_letter_in_word = False
            for i in self.letter_list:
                if i.letter == input_letter:
                    self.is_letter_in_word = True
                    i.open_flag = True
                new_word += i.show()
            return new_word

    def game_mechanics(self, show_word_flag, input_letter):   #механика игры
        new_word = self.show(show_word_flag, input_letter)
        self.check(input_letter)
        self.decrease_attemts(input_letter)
                
        return (new_word, self.attemts_number)

class Letter():                                      #каждая буква как класс
    def __init__(self, letter, open_flag):
        self.letter = letter
        self.open_flag = open_flag
    
    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state['letter'] = self.letter
        state['open_flag'] = self.open_flag
        return state

    def __setstate__(self, state: dict):  # Как мы будем восстанавливать класс из байтов
        self.letter = state['letter']
        self.open_flag = state['open_flag'] 

    def show(self):                         #открытие или закрытие буквы
        if self.open_flag:
            return self.letter
        else:
            return '*'

def game(levels_dict):
    os.system('cls')                                        #функция игры
    print('New game - 1\nContinue game - 2\nDeleting saves - 3\n')
    gamer_input = getGamerInput(True, True)               #начать новую игру или продолжить
    os.system('cls')
    is_continue = False
    if gamer_input == 2 or gamer_input == 3:
        print('Select save\n')
        getFiles(r'C:\Users\1\Desktop\яжпрограммист\Iskander\Github\Games\Висилица\save')                                    #вывести все файлы, содержащиеся в папке 
        while not is_continue:
            number_file = getNumber_save(r'C:\Users\1\Desktop\яжпрограммист\Iskander\Github\Games\Висилица\save')                 #получить номер файла в папке
            os.system('cls')
            for i in files_list:
                if i.number == number_file:
                    file = i
                    if gamer_input == 3:                        #удаление выбранного сохранения
                        file.delete()
                        is_continue = True
                        game(levels_dict)
                    else:
                        gamer_choice = file.name
                        break
            if not is_continue:
                try:                                                #проверка на возможность чтения файла
                    game_params = reading(r'C:\Users\1\Desktop\яжпрограммист\Iskander\Github\Games\Висилица\save',\
                         gamer_choice)
                    is_continue = True
                except:
                    print('Error, try again')

        slovo = game_params[0]                              #сохраненные параметры игры
        level = game_params[1]
        input_number = game_params[2]
        attemts_number = slovo.attemts_number
                
    elif gamer_input == 1:
        print(f'Select difficulty level:\
            {edit_level_sentence(levels_dict, 1)} (Press 1)\
            {edit_level_sentence(levels_dict, 2)} (Press 2)\
            {edit_level_sentence(levels_dict, 3)} (Press 3)')       #вывод уровней

        gamer_input = getGamerInput(True, False)                     # ввод уровня
        os.system('cls')

        level = gamer_input                             #параметры игры
        word = levels_dict[str(level)][3]
        attemts_number = levels_dict[str(level)][2]
        slovo = Slovo(word, attemts_number)
        input_number = 0

    print(edit_level_sentence(levels_dict, level))                #вывод параметров игры
    print(slovo.show(False), f'\nAttempts left: {attemts_number}')
    
    while attemts_number != 0:                                   #пока количество ходов не равно 0
        gamer_input = getGamerInput(False, False)
        os.system('cls')
        if gamer_input == 'save':                                #сохранение
            print('Enter the name of the save')
            recording(input(), slovo, level, input_number) 
            return print('\nSee you')
        input_number += 1

        new_word, attemts_number = slovo.game_mechanics(False, gamer_input)     #получение слова
        print(f'{new_word} \nAttempts left: {attemts_number}')

        if new_word == slovo.show(True):                                     #условие выйгрыша
            print(f'\nCongratulations\nYou win\nYou completed the game in {input_number} turns')
            break
        
    if attemts_number == 0:         #если игрок проиграл
        print('\nGame over')
    
    if is_continue:                                                      #если использовал сохранение
        print('\nDo you want to delete this save?\nYes - 1\nNo - 2\n')     #предложение удалить сохранение
        gamer_input = getGamerInput(False, True)
        os.system('cls')
        if gamer_input == 1:
            file.delete()
        
    print('\nDo you want to start a new game?\nYes - 1\nNo - 2\n')       #предложение начать новую игру
    gamer_input = getGamerInput(False, True)
    os.system('cls')
    if gamer_input == 1:
        game(levels_dict)
    else:
        return print('Goodbye')


class File():                                          #каждый файл в папке как класс
    def __init__(self, name, folder, number):
        self.name = name
        self.number = number
        self.folder = folder
    
    def delete(self):                             #функция удаления файла
        os.remove(f'{self.folder}\{self.name}')
    
    def getDate(self):                           #получение даты файла
        return time.ctime(os.path.getmtime(f'{self.folder}\{self.name}'))
    


def getFiles(folder):                                    #получить все файлы в папке
    global files_list
    files_list = os.listdir(folder)
    file_number = 1
    for file in files_list:
        file = File(file, folder, file_number)
        date = file.getDate()
        files_list[files_list.index(file.name)] = file
        print(f'{file.name} {date} (Press {file.number})')
        file_number += 1
    if file_number == 1:
        print('Error, try again')
        return game(levels_dict)


def recording(name, *elements):                         #функция записи сохранения
    with open(r'C:\Users\1\Desktop\яжпрограммист\Iskander\Github\Games\Висилица\save\\'+ name, "wb") as fp:
        pickle.dump(elements, fp)
    
def reading(folder, file):                               #функция чтения сохранения
    with open(f'{folder}\{file}', "rb") as fp:
        return pickle.load(fp)

def edit_level_sentence(dict, level):                           #функция для длинных предложений
    return f'\n{dict[str(level)][0]} - The word consists of {dict[str(level)][1]} letters, \
the number of attempts is {dict[str(level)][2]}'

levels_dict = {'1': ['Easy', 5, 9, 'apple'], \
               '2': ['Normal', 7, 7, 'shelter'], \
               '3': ['Hard', 9, 7, 'binominal']}                #словарь загаданный слов, с различными уровнями                 

game(levels_dict)                                      #запуск игры

