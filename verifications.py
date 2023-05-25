import validators
import os
from rich.console import Console

rich_console = Console().print


def check_user_input_source(site_or_file):
    """Функция проверки введённого значения пользователем для определения источника.
    :param site_or_file: Пользовательский ввод для проверки"""

    if site_or_file.isdigit() and site_or_file in ('1', '2'):
        return site_or_file
    elif site_or_file.isdigit() is False or site_or_file not in ('1', '2'):
        rich_console('Указано неверное значение. Пожалуйста, укажите откуда брать информацию для анализа.')
        rich_console('Введите [cyan]1[/cyan], если нужно проанализировать HTML-код с сайта, '
                     'или введите [cyan]2[/cyan], если нужно считать из файла: ', style='yellow')
        site_or_file = input()
        return check_user_input_source(site_or_file)


def check_site_address(url: str):
    """Функция проверки введённого URL сайта.
    :param url: Пользовательский ввод для проверки"""

    if validators.url(url):
        return url
    else:
        rich_console('Введён неверный URL сайта.', style='yellow')
        rich_console('Пожалуйста, введите верный адрес сайта (пример: https://google.com): ', style='cyan')
        url = input()
        return check_site_address(url)


def check_file_path(path: str):
    """Функция проверки введённого пути к файлу.
    :param path: Путь к файлу. Ex.: C:\\Windows\\etc\\hosts"""

    if os.path.exists(path) and path.split('.')[-1] in ('html', 'txt'):
        return path
    else:
        rich_console('Указан неверный путь к файлу или указано неверное имя|расширение файла.', style='yellow')
        rich_console('Введите корректный путь к файлу: ', style='cyan')
        path = input('')
        return check_file_path(path)


def check_input(is_user_agree):
    """Функция проверки введённого положительного или отрицательного ответа
    :param is_user_agree: """

    if is_user_agree in ('yes', 'да'):
        return is_user_agree
    elif is_user_agree in ('no', 'нет'):
        return is_user_agree
    else:
        rich_console('Не удалось распознать ответ. Введите [green]yes|да[/green] или [red]no|нет[/red]:', style='yellow')
        return check_input(input())
