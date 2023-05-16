import json
import site_analyzer
import verifications
import os
from sys import exit

tag_list_single = ('header', 'nav', 'main', 'article', 'section', 'aside', 'footer',
                   'form', 'label', 'table', 'caption', 'h2', 'h3', 'h4', 'h5', 'h6',
                   'thead', 'tbody', 'tfoot', 'th', 'tr', 'td')
tag_list_multi = ('h1', 'strong', 'em')
tag_list_multi_with_attr = ({'input': ('name', 'id', 'type', 'value')},
                            {'img': ('alt', 'title')}, {'ul': 'li', 'ol': 'li'})


print('Укажите, откуда брать данные для анализа сайта?')
user_input = input('Если с сайта, то введите - 1, если из файла - введите 2: ')
if verifications.check_user_input_source(user_input) == '1':
    print('Введите URL сайта, который нужно проанализировать.')
    site_url = input('URL сайта: ')
    if verifications.check_site_address(site_url):
        site_data = site_analyzer.parser_source('site', site_url)
        result1 = site_analyzer.single_tag_processor(tag_list_single, site_data)
        result2 = site_analyzer.multi_tag_processor(tag_list_multi, site_data)
        result3 = site_analyzer.multi_tag_with_attr_processor(tag_list_multi_with_attr, site_data)

        result_dict = dict()
        result_dict |= result1
        result_dict |= result2
        result_dict |= result3

        json_object = json.dumps(result_dict)

        file = open('result.json', 'w')
        file.write(json_object)
        file.close()

elif verifications.check_user_input_source(user_input) == '2':
    print('Введите путь к файлу, который нужно считать и проанализировать.')
    file_path = input('Файл должен быть расширения .txt либо .html: ')
    if verifications.check_file_path(file_path):
        site_data = site_analyzer.parser_source('file', file_path)
        result1 = site_analyzer.single_tag_processor(tag_list_single, site_data)
        result2 = site_analyzer.multi_tag_processor(tag_list_multi, site_data)
        result3 = site_analyzer.multi_tag_with_attr_processor(tag_list_multi_with_attr, site_data)

        result_dict = dict()
        result_dict |= result1
        result_dict |= result2
        result_dict |= result3

        json_object = json.dumps(result_dict)

        file = open('result.json', 'w')
        file.write(json_object)
        file.close()


input(f'Разложен по тегам в файл result.json по пути {os.getcwd()}'
      f'\nПарсер закончил работу. Нажмите Enter...')
exit()
