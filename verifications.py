from validators import url
import os
from rich.console import Console

rich_console = Console().print


def check_user_input_source(data_to_check):
    if data_to_check.isdigit and data_to_check in ('1', '2'):
        return data_to_check
    elif data_to_check.isdigit is False or data_to_check not in ('1', '2'):
        rich_console('Указано неверное значение. Пожалуйста, укажите откуда брать информацию для анализа.')
        rich_console('Введите [cyan]1[/cyan], если нужно проанализировать HTML-код с сайта, '
                     'или введите [cyan]2[/cyan], если нужно считать из файла: ', style='yellow')
        user_input = input()
        return check_user_input_source(user_input)


def check_site_address(data_to_check):
    if url(data_to_check):
        return data_to_check
    else:
        rich_console('Введён неверный URL сайта.', style='yellow')
        rich_console('Пожалуйста, введите верный (пример: https://google.com): ', style='cyan')
        data_to_check = input()
        return check_site_address(data_to_check)


def check_file_path(path):
    if os.path.exists(path) and path.split('.')[-1] in ('html', 'txt'):
        return path
    else:
        rich_console('Указан неверный путь к файлу или указано неверное имя|расширение файла.', style='yellow')
        rich_console('Введите корректный путь к файлу: ', style='cyan')
        path = input('')
        return check_file_path(path)


def check_input(data_to_check):
    if data_to_check in ('Y', 'y', 'Д', 'д'):
        return data_to_check
    elif data_to_check in ('N', 'n', 'Н', 'н'):
        return data_to_check
    else:
        rich_console('Не удалось распознать ответ. Введите [green]y|д[/green] или [red]n|н[/red]:', style='yellow')
        return check_input(input())
