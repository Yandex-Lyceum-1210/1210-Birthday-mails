from config.settings_handler import SenderConfig
from PyQt5.QtWidgets import QApplication
import sys


def except_hook(cls, exception, traceback):  # Выводит необработанные ошибки
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':  # Запуск окна настроек отправителя при запуске программы
    app = QApplication(sys.argv)
    sender_config_window = SenderConfig()
    sender_config_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
