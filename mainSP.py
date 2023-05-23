import json
import site_analyzer
import verifications
import os
from sys import exit
import table_creator
from rich.console import Console

rich_console = Console().print

__version__ = '1.0.0'


def main():
    tag_list_single = ('header', 'nav', 'main', 'article', 'section', 'aside', 'footer',
                       'form', 'label', 'table', 'caption', 'h2', 'h3', 'h4', 'h5', 'h6',
                       'thead', 'tbody', 'tfoot', 'th', 'tr', 'td')
    tag_list_multi = ('h1', 'strong', 'em')
    tag_list_multi_with_attr = ({'input': ('name', 'id', 'type', 'value')},
                                {'img': ('alt', 'title')}, {'ul': 'li', 'ol': 'li'})

    rich_console("Укажите, откуда брать данные для анализа сайта?", style='yellow')
    rich_console("[yellow]Если с сайта, то введите - 1[/yellow], если [cyan]из файла - введите 2[/cyan]: ")
    user_input = verifications.check_user_input_source(input())
    if user_input == '1':
        rich_console('Введите URL сайта, который нужно проанализировать: ', style='yellow')
        site_url = verifications.check_site_address(input())
        site_data = site_analyzer.parser_source('site', site_url)
        single_tag = site_analyzer.single_tag_processor(tag_list_single, site_data)
        multi_tag = site_analyzer.multi_tag_processor(tag_list_multi, site_data)
        multi_tag_attr = site_analyzer.multi_tag_with_attr_processor(tag_list_multi_with_attr, site_data)

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

        html_data = dict()
        html_data |= single_tag
        html_data |= multi_tag
        html_data |= multi_tag_attr

        table_creator.create_table_single_tag(html_data)
        table_creator.create_table_multi_tag(html_data)
        table_creator.create_table_tag_attr_multi(html_data)

    rich_console("[yellow]Сохранить результат анализа как json файл?[/yellow] "
                 "[bold red]Cуществующий файл будет перезаписан! [/bold red]"
                 "[yellow]Введите [green]y|д[/green] или [red]n|н[/red]:[/yellow] ")
    save_file = verifications.check_input(input())
    if save_file.lower() in ('y', 'д'):
        json_object = json.dumps(html_data)

        file = open('result.json', 'w')
        file.write(json_object)
        file.close()

        rich_console(f'HTML-код разложен по тегам в файл [cyan]result.json[/cyan] по пути {os.getcwd()}', style='yellow')

    rich_console(f'Анализатор закончил работу.\nЗапустить новый анализ? Введите [green]y|д[/green] или [red]n|н[/red]:')
    new_start = verifications.check_input(input()).lower()
    if new_start in ('y', 'д'):

        rich_console('Произвести очистку консольного окна перед началом нового анализа? '
                     'Введите [green]y|д[/green] или [red]n|н[/red]:', style='yellow')

        if verifications.check_input(input()) in ('y', 'д'):
            os.system('cls')
        main()

    elif new_start in ('n', 'н'):
        rich_console('В таком случае анализатор завершает свою работу.\n '
                     'Нажмите Enter для закрытия консольного окна...', style='yellow')
        input()
        exit()


try:
    rich_console(f'Начать анализ HTML-кода? Введите [green]y|д[/green] или [red]n|н[/red]:', style='yellow')
    start = verifications.check_input(input()).lower()
    if start in ('y', 'д'):
        main()
    elif start in ('n', 'н'):
        rich_console('В таком случае анализатор завершает свою работу.\n'
                     'Нажмите Enter для закрытия консольного окна...', style='red')
        input()
        exit()
except KeyboardInterrupt:
    exit()


