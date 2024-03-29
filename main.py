import json
import os
from sys import exit
from rich.console import Console
import time

import site_analyzer
import verifications
import table_creator
import formula_expression

rich_console = Console().print

__version__ = '1.0.1'


def main():
    """основной код программы"""

    tag_list_single = ('header', 'nav', 'main', 'article', 'section', 'aside', 'footer',
                       'form', 'label', 'table', 'caption', 'h2', 'h3', 'h4', 'h5', 'h6',
                       'thead', 'tbody', 'tfoot', 'th', 'tr', 'td')
    tag_list_multi = ('h1', 'strong', 'em')
    tag_list_multi_with_attr = ({'input': ('name', 'id', 'type', 'placeholder')},
                                {'img': ('alt', 'title')}, {'ul': 'li', 'ol': 'li'})

    rich_console("Укажите, откуда брать данные для анализа сайта?", style='yellow')
    rich_console("Если [yellow]с сайта, то введите - 1[/yellow], если [cyan]из файла - введите 2[/cyan]: ")
    user_input = verifications.check_user_input_source(input())
    if user_input == '1':
        rich_console('Введите URL сайта, который нужно проанализировать: ', style='yellow')
        site_url = verifications.check_site_address(input())
        site_data = site_analyzer.parser_source('site', site_url)
        single_tag = site_analyzer.single_tag_processor(tag_list_single, site_data)
        multi_tag = site_analyzer.multi_tag_processor(tag_list_multi, site_data)
        multi_tag_attr = site_analyzer.multi_tag_with_attr_processor(tag_list_multi_with_attr, site_data)

        # объединяем словари, нужно для построения таблицы и для формулы
        html_data = dict()
        html_data |= single_tag
        html_data |= multi_tag
        html_data |= multi_tag_attr

        table_creator.create_table_single_tag(html_data)
        table_creator.create_table_multi_tag(html_data)
        table_creator.create_table_tag_attr_multi(html_data)

    elif user_input == '2':
        rich_console('Введите путь к файлу, который нужно считать и проанализировать.', style='yellow')
        rich_console('Файл должен быть расширения [cyan].txt либо .html[/cyan]: ', style='yellow')
        file_path = verifications.check_file_path(input())
        site_data = site_analyzer.parser_source('file', file_path)
        single_tag = site_analyzer.single_tag_processor(tag_list_single, site_data)
        multi_tag = site_analyzer.multi_tag_processor(tag_list_multi, site_data)
        multi_tag_attr = site_analyzer.multi_tag_with_attr_processor(tag_list_multi_with_attr, site_data)

        # объединяем словари, нужно для построения таблицы и для формулы
        html_data = dict()
        html_data |= single_tag
        html_data |= multi_tag
        html_data |= multi_tag_attr

        table_creator.create_table_single_tag(html_data)
        table_creator.create_table_multi_tag(html_data)
        table_creator.create_table_tag_attr_multi(html_data)

    rich_console("[yellow]Сохранить результат анализа как json файл?[/yellow] "
                 "[bold red]Cуществующий файл будет перезаписан! [/bold red]"
                 "[yellow]Введите [green]yes|да[/green] или [red]no|нет[/red]:[/yellow] ")

    save_file = verifications.check_input(input())
    if save_file.lower() in ('yes', 'да'):
        json_object = json.dumps(html_data)

        file = open('result.json', 'w')
        file.write(json_object)
        file.close()

        rich_console(f'HTML-код разложен по тегам в файл [cyan]result.json[/cyan] по пути {os.getcwd()}',
                     style='yellow')

    formula_expression.formula(html_data)

    rich_console(f'Анализатор закончил работу.\nЗапустить новый анализ? Введите '
                 f'[green]yes|да[/green] или [red]no|нет[/red]:')
    new_start = verifications.check_input(input()).lower()
    if new_start in ('yes', 'да'):

        rich_console('Произвести очистку консольного окна перед началом нового анализа? '
                     'Введите [green]yes|да[/green] или [red]no|нет[/red]:', style='yellow')

        if verifications.check_input(input()) in ('yes', 'да'):
            os.system('cls')
        main()

    elif new_start in ('no', 'нет'):
        rich_console('В таком случае анализатор завершает свою работу. \n'
                     'Нажмите Enter для закрытия консольного окна...', style='yellow')
        input()
        exit()


try:
    rich_console(f'Начать анализ HTML-кода? Введите [green]yes|да[/green] или [red]no|нет[/red]:', style='yellow')
    start = verifications.check_input(input()).lower()
    if start in ('yes', 'да'):
        main()
    elif start in ('no', 'нет'):
        rich_console('В таком случае анализатор завершает свою работу.\n'
                     'Нажмите Enter для закрытия консольного окна...', style='red')
        input()
        exit()

# реагируем на нажатие CTRL+C (станд.сочетание клавиш для прекращения работы консольного приложения)
except KeyboardInterrupt:
    rich_console('Закрытие программы. Причина: нажатие сочетания клавиш CTRL+C', style='red')
    time.sleep(5)
    exit()
