# TODO: FINALLY: replace .ui files with .py files
from config.program_config import PATH
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow
from time import sleep
CONFIG_FILE = 'config/configurations.bm'  # Путь до файла конфигурации


class SenderConfig(QMainWindow):  # Класс окна настроек отправителя
    def __init__(self):
        super(SenderConfig, self).__init__()
        uic.loadUi('config/sender_config.ui', self)
        sleep(10)
        self.textEditorWindow = None  # Экземпляр окна редактора текста и темы. Пока не вызывается
        self.buttonBox.accepted.connect(self.save_sender_config)  # Отменить
        self.buttonBox.rejected.connect(self.cancel_sender_config)  # Сохранить
        self.textEditorWindowBtn_3.triggered.connect(self.openTextEditorWindow)  # Переход к окну редактора текста
        # и темы через меню

    def save_sender_config(self):  # Функция сохранения настроек
        import configparser
        import os
        import codecs
        name_from, email_from = self.name_from.text(), self.email_from.text()
        password, server, port = self.password.text(), self.server.text(), self.port.text()
        name_from = '=?UTF-8?B?' + \
                    str(codecs.encode(bytes(name_from, encoding='UTF-8'), encoding='base64'))[2:-3] +\
                    '?='  # преобразование имени отправителя в header в соответствии со стандартом RFC
        verify_answer = self.verify(name_from, email_from, password, server, port)  # Проверка корректности
        # введённых данных
        if verify_answer != 0:
            self.show_message(QMessageBox.Critical, "Ошибка", "Ошибка!", verify_answer)
        else:
            if not os.path.exists(CONFIG_FILE):
                self.show_message(QMessageBox.Critical, "Ошибка выполнения", "Ошибка!",
                                  str('Файл конфигурации \'' + CONFIG_FILE + '\' не найден!'))
            else:
                config = configparser.ConfigParser()
                config.read(CONFIG_FILE)
                try:  # Сохранение данных в файл конфигурации configurations.bm
                    config.set('sender', 'name_from', name_from)
                    config.set('sender', 'email_from', email_from)
                    config.set('sender', 'password', password)
                    config.set('sender', 'server', server)
                    config.set('sender', 'port', port)
                except configparser.NoSectionError:
                    self.show_message(QMessageBox.Critical, "Ошибка выполнения", "Ошибка!",
                                      'В файле конфигурации отсутствуют нужные секции!')
                try:
                    with open(CONFIG_FILE, "w") as config_file:
                        config.write(config_file)
                except BaseException:
                    self.show_message(QMessageBox.Critical, "Ошибка", "Ошибка! Изменения не сохранены")
                else:
                    self.show_message(QMessageBox.Information, "Сохранено", "Настройки успешно сохранены")

    @staticmethod
    def verify(name_from, email_from, password, server, port):  # Проверка корректности введённых данных
        from validate_email import validate_email
        if name_from == '=?UTF-8?B??=':
            return 'Заполните имя отправителя'
        if not validate_email(email_from):
            return 'Несуществующий Email-адрес отправителя'
        if password == '':
            return 'Заполните поле пароля'
        if '.' not in server:
            return 'Неверный формат адреса сервера'
        try:
            port == int(port)
        except ValueError:
            return 'Неверный формат порта'
        return 0  # Все данные введены корректно

    @staticmethod
    def show_message(ttype, title, text, description=None):  # Открытие окна ошибки
        msg = QMessageBox()
        msg.setIcon(ttype)
        msg.setText(text)
        if description:
            msg.setInformativeText(description)
        msg.setWindowTitle(title)
        msg.exec_()

    def cancel_sender_config(self):  # Обработчик кнопки "Отмена"
        self.hide()

    def openTextEditorWindow(self):  # Открывает окно редактора текста и темы письма
        self.textEditorWindow = TextEditor()  # Экземпляр окна редактора текста и темы
        self.textEditorWindow.show()
        self.hide()


class TextEditor(QMainWindow):  # Класс редактора текста и темы письма
    def __init__(self):
        super(TextEditor, self).__init__()
        uic.loadUi('config/text_editor.ui', self)
        self.senderConfigWindow = None  # Экземпляр окна настроек отправителя. Пока не вызывается
        self.buttonBox.accepted.connect(self.save_text)  # Сохранить
        self.buttonBox.rejected.connect(self.cancel_text)  # Отменить
        self.senderConfigWindowBtn.triggered.connect(self.openSenderConfigWindow)  # Открытие окна настроек отправителя
        self.bold.stateChanged.connect(self.bold_text)  # Галочка полужирного текста
        self.italic.stateChanged.connect(self.italic_text)  # Галочка курсива
        self.underlined.stateChanged.connect(self.underlined_text)  # Галочка подчёркивания

    def bold_text(self):  # Добавляет html-тег <b>, чтобы сделать шрифт полужирным
        if self.sender().isChecked():
            self.textEdit.insertPlainText('<b>')
        else:
            self.textEdit.insertPlainText('</b>')

    def italic_text(self):  # Добавляет html-тег <i>, чтобы сделать шрифт полужирным
        if self.sender().isChecked():
            self.textEdit.insertPlainText('<i>')
        else:
            self.textEdit.insertPlainText('</i>')

    def underlined_text(self):  # Добавляет html-тег <u>, чтобы сделать шрифт полужирным
        if self.sender().isChecked():
            self.textEdit.insertPlainText('<u>')
        else:
            self.textEdit.insertPlainText('</u>')

    def save_text(self):  # Обработчик кнопки "Сохранить"
        import configparser
        import os
        if not os.path.exists(CONFIG_FILE):
            self.show_message(QMessageBox.Critical, "Ошибка выполнения", "Ошибка!",
                              str('Файл конфигурации \'' + CONFIG_FILE + '\' не найден!'))
        else:
            import codecs
            subject = '=?UTF-8?B?' + \
                      str(codecs.encode(bytes(self.subject.text(), encoding='UTF-8'),
                                        encoding='base64'))[2:-3] + '?='  # Преобразовывает тему в header
            # в соответствии со стандартом RFC
            if self.randtext.isChecked():  # Состояние галочки случайного текста
                text = '*random*'
            else:
                text = self.textEdit.toPlainText().replace('\n', '<br>')
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            if text != '':  # Если поле текста заполнено или был выбран случайный текст,
                # производится запись. При пустом поле данные о тексте не изменятся
                try:
                    config.set('letter', 'text', text)  # Запись текста в файл конфигурации
                except configparser.NoSectionError:
                    self.show_message(QMessageBox.Critical, "Ошибка выполнения", "Ошибка!",
                                      'В файле конфигурации отсутствуют нужные секции!')
                    return
            if subject != '':  # При заполненом поле темы производится запись данных
                try:
                    config.set('letter', 'subject', subject)  # Запись данных в файл конфигурации
                except configparser.NoSectionError:
                    self.show_message(QMessageBox.Critical, "Ошибка выполнения", "Ошибка!",
                                      'В файле конфигурации отсутствуют нужные секции!')
                    return
            try:
                with open(CONFIG_FILE, "w") as config_file:
                    config.write(config_file)
            except BaseException:
                self.show_message(QMessageBox.Critical, "Ошибка", "Ошибка! Изменения не сохранены")
            else:
                self.show_message(QMessageBox.Information, "Сохранено", "Настройки успешно сохранены")

    @staticmethod
    def show_message(ttype, title, text, description=None):  # Показывает окно ошибки
        msg = QMessageBox()
        msg.setIcon(ttype)
        msg.setText(text)
        if description:
            msg.setInformativeText(description)
        msg.setWindowTitle(title)
        msg.exec_()

    def cancel_text(self):  # Обработчик кнопки "Отмена"
        self.hide()

    def openSenderConfigWindow(self):  # Открыть окно настроек отправителя
        self.senderConfigWindow = SenderConfig()  # Экземпляр окна настроек отправителя
        self.senderConfigWindow.show()
        self.hide()


def except_hook(cls, exception, traceback):  # Выводит необработанные ошибки
    sys.__excepthook__(cls, exception, traceback)

