from validators import url
import os
from rich.console import Console

rich_console = Console().print

def check_user_input_source(data_to_check):
    if data_to_check.isdigit and data_to_check in ('1', '2'):
        return data_to_check
    elif data_to_check.isdigit is False or data_to_check not in ('1', '2'):
        print('Указано неверное значение. Пожалуйста, укажите откуда брать информацию для анализа.')
        user_input = input('Введите 1, если нужно проанализировать HTML-код с сайта, или введите 2, если нужно считать '
                           'из файла: ')
        return check_user_input_source(user_input)


def check_site_address(data_to_check):
    if url(data_to_check):
        return True
    else:
        print('Введён неверный URL сайта.')
        return check_site_address(input('Пожалуйста, введите верный (пример: https://google.com): '))


def check_file_path(path):
    if os.path.exists(path) and path.split('.')[-1] in ('html', 'txt'):
        return True
    else:
        print('Указан неверный путь к файлу или указано неверное имя|расширение файла.')
        path = input('Введите корректный путь к файлу: ')
        return check_file_path(path)


def check_input(data_to_check):
    if data_to_check in ('Y', 'y', 'N', 'n', 'Д', 'д', 'Н', 'н'):
        return True
    else:
        rich_console(r'Не удалось распознать ответ. Введите y\д или n\н:')
        data_to_check = input()
        return check_input(data_to_check)
