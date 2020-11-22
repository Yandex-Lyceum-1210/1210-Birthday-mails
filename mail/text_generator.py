import datetime
import time
from random import randrange
import csv
import sys


class PostcardMaker:
    def __init__(self):
        self.wishes = [['Пусть даже в холодный день вас всегда греет любовь близких! С Днём рождения!'],
                       ['Весной расцветают лучшие букеты! С Днём рождения!'],
                       ['Жалко, что Вы сейчас не в школе, мы скучаем по Вам. С Днём рождения!'],
                       ['Желаем Вам успехов и счастья! С Днём рождения!']]

    def do(self):  # данная функция выбирает случайное поздравление в зависимости от времни года
        time = str(datetime.datetime.now()).split()
        time = time[0]
        time = time.split('-')
        months = int(time[1])
        if months == 12 or months == 1 or months == 2:
            wish_number = randrange(0, len(self.wishes[0]))
            return self.wishes[0][wish_number]
        elif months == 3 or months == 4 or months == 5:
            wish_number = randrange(0, len(self.wishes[1]))
            return self.wishes[1][wish_number]
        elif months == 6 or months == 7 or months == 8:
            wish_number = randrange(0, len(self.wishes[2]))
            return self.wishes[2][wish_number]
        elif months == 9 or months == 10 or months == 11:
            wish_number = randrange(0, len(self.wishes[3]))
            return self.wishes[3][wish_number]
