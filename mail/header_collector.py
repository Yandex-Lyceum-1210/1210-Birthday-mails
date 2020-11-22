def collect_headers(to_mail, name):  # Функция, собирающая содержимое письма
    import os
    from mail.send import send
    import configparser
    from config.program_config import PATH
    greeting = 'Здравствуйте'
    if len(name.split()) > 1:
        name = ' '.join(name.split()[1:])
    config = configparser.ConfigParser()
    config_path = 'config/configurations.bm'  # Путь к файлу конфигурации
    if not os.path.exists(config_path):
        return str('Файл конфигурации \'' + config_path + '\' не найден!')
    else:
        config.read(config_path)
    template = config.get('letter', 'template')
    template = 'html_templates/index.html'
    if not os.path.exists(template):
        print('Файл с шаблоном письма \'' + template + '\' не найден!')
    else:
        html_file = open(template, encoding='UTF-8')
        html = html_file.read()  # Запись html-шаблона письма в текстовую переменную
        html_file.close()
        if os.path.exists(config_path):
            config.read(config_path)
            try:
                text = config.get('letter', 'text')
                subject = config.get('letter', 'subject')
                name_from = config.get('sender', 'name_from')
                email_from = config.get('sender', 'email_from')
                password = config.get('sender', 'password')
                server = config.get('sender', 'server')
                port = config.get('sender', 'port')
            except configparser.NoSectionError:
                return 'В файле конфигурации отсутствуют нужные секции!'
            else:
                # Если отсутствуют данные об отправителя, используем данные по умолчанию для демо-отправителя
                if server == '' or port == '' or password == '' or email_from == '' or name_from == '':
                    server = 'smtp.gmail.com:587'
                    name_from = '1210 School'
                    email_from = 'notifications.1210@gmail.com'
                    password = 'D2D-HHa-7Dp-xPH'
                else:
                    server += ':' + str(port)
                if text == '*random*':  # Если используется случайный текст, генерируем его
                    from mail.text_generator import PostcardMaker
                    text = PostcardMaker().do()
                signature = '<br>Ваша любимая<br>Школа №1210'
                # Замена частей шаблона актуальными данными. (format() применить не удалось, так как
                # в шаблоне присутствуют фигурные скобки не только там, где нужно заменить текст
                html = html.replace('{greeting}', greeting).replace('{name}', name).replace('{text}',
                                                                                            text).replace('{signature}',
                                                                                                          signature)
                answer = send(to_mail, subject, html, fromname=name_from, server=server,
                              frommail=email_from, pwd=password)  # Отправляем письмо, получаем результат отправки
                if 'Сообщение успешно отправлено адресату ' in answer:
                    return True
                else:
                    return False


if __name__ == '__main__':  # При запуске этой программы выполнится тест с указанными ниже данными
    collect_headers('aksenovn@s1210.ru', 'Никита')
