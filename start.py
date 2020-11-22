import datetime
import time
import csv
import configparser
from config.program_config import PATH


class Main:
    def __init__(self):
        self.names = []
        self.emails = []

    def start_sending(self):
        from mail.header_collector import collect_headers
        if CheckTime().timer():
            users_info = Users().address_founder()
            for element in users_info:
                self.names.append(element[0])
                self.emails.append(element[1])
            if len(self.names) != 0:
                for i in range(len(self.names)):
                    if collect_headers(self.emails[i], self.names[i]):
                        global donepeople
                        donepeople.append(self.emails[i])
            else:
                pass
        else:
            donepeople.clear()


class CheckTime(Main):
    def __init__(self):
        super().__init__()
        self.flag = True

    def check_time(self):  # данная функция даёт добро на создание открытки, если есть хотя бы 10 часов утра
        time = str(datetime.datetime.now()).split()
        if time[1] > '10:00:00.0':
            self.flag = False
            return True
        return False

    def timer(self):  # данная функция каждый час запускает проверку на время
        while self.flag:
            return self.check_time()


class Users(Main):  # это класс, возвращающий данные о именинниках (почта и имя)
    def __init__(self):
        super().__init__()
        self.users, self.list = None, None

    def address_founder(self):
        with open('Открытки. База данных - List.csv', encoding="utf8") as csvfile:
            self.users = csv.reader(csvfile, delimiter=',', quotechar='"')
            self.list = []
            for index, row in enumerate(self.users):
                self.list.append(row)
        ttime = str(datetime.datetime.now()).split()
        ttime = ttime[0]
        ttime = ttime.split('-')
        bday = []
        for element in self.list:
            if element != self.list[0]:
                date = element[5].split('.')
                name = element[1] + ' ' + element[2] + ' ' + element[3]
                email = element[4]
                global donepeople
                if email not in donepeople:
                    if date[0] == ttime[2] and date[1] == ttime[1]:
                        user = []
                        if element[4] == '':
                            user.append(name)
                            user.append(None)
                            bday.append(user)
                        else:
                            user.append(name)
                            user.append(element[4])
                            bday.append(user)
        return bday


CONFIG_FILE = 'config/configurations.bm'
while True:
    config = configparser.ConfigParser()
    try:
        d = config.read(CONFIG_FILE)
        donepeople = config.get('sent', 'donepeople').split(', ')
    except configparser.NoSectionError as e:
        print(e, d)
        time.sleep(10)
        continue
    Main().start_sending()
    try:  # Сохранение обработанных адресатов в конфигурационный файл
        config.set('sent', 'donepeople', ', '.join(donepeople))
    except configparser.NoSectionError:
        print('В файле конфигурации отсутствуют нужные секции!')
        continue
    try:
        with open(CONFIG_FILE, "w") as config_file:
            config.write(config_file)

    except BaseException as e:
        print("Ошибка! Изменения не сохранены", e)
        continue
    print('ok')
    break
