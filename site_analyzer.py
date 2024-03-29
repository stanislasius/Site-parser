import bs4
import requests
import web_handler


def parser_source(source, data):
    """Функция для определения источника полученных данных
    :param source: источник данных
    :param data: данные для парсинга с помощью bs4(beautifulsoup4)"""

    if source == 'site':
        data = web_handler.check_site(data)
        response = requests.get(data, allow_redirects=True)
        data = bs4.BeautifulSoup(response.text, 'html5lib')
    elif source == 'file':
        file = open(data, 'r', encoding='utf-8')
        data = bs4.BeautifulSoup(file, 'html5lib')
        file.close()

    return data


def single_tag_processor(tag_list, html_data):
    """Функция для обработки тегов на наличие/отсутствие оных
    :param tag_list: список тегов, по которым нужно провести анализ
    :param html_data: html-код для анализа"""

    tag_dict = dict()
    for tag in tag_list:
        if html_data.find(tag) is not None:
            tag_dict[tag] = True
        else:
            tag_dict[tag] = False
    return tag_dict


def multi_tag_processor(tag_list, html_data):
    """Функция для обработки тегов em, strong, h1. На вход принимает:
    :param tag_list: список тегов, по которым нужно провести анализ
    :param html_data: html-код для анализа"""

    tag_dict = dict()
    em_text = list()
    strong_text = list()
    h1_text = list()

    for tag in tag_list:
        # находим все упоминания нужного tag во всём html-коде
        if len(html_data.findAll(tag)) != 0:
            tag_len = len(html_data.findAll(tag))
            # получаем текст, который "обёрнут" в соответствующие теги
            if tag == 'em':
                for text in html_data.find_all('em'):
                    text = str(text)[4:-5]
                    if len(text) > 0:
                        tag_dict[tag] = {'Text': ''}
                        if '\n' in text:
                            text = text.replace('\n', '')
                        if ' ' in text:
                            text = ' '.join(text.split())
                        em_text.append(text)
                else:
                    tag_dict[tag] = {'Текст': em_text}
                    tag_dict[tag].update(total=f'{tag_len}')
            elif tag == 'strong':
                for text in html_data.find_all('strong'):
                    text = str(text)[8:-9]
                    if len(text) > 0:
                        if '\n' in text:
                            text = text.replace('\n', '')
                        if ' ' in text:
                            text = ' '.join(text.split())
                        strong_text.append(text)
                else:
                    tag_dict[tag] = {'Текст': strong_text}
                    tag_dict[tag].update(total=f'{tag_len}')
            elif tag == 'h1':
                for text in html_data.find_all('h1'):
                    text = str(text)[4:-5]
                    if len(text) > 0:
                        if '\n' in text:
                            text = text.replace('\n', '')
                        if ' ' in text:
                            text = ' '.join(text.split())
                        h1_text.append(text)
                else:
                    tag_dict[tag] = {'Текст': h1_text}
                    tag_dict[tag].update(total=f'{tag_len}')
        else:
            # если тег не был найден
            tag_dict[tag] = False
    return tag_dict


def multi_tag_with_attr_processor(tag_list, html_data):
    """Функция для обработки тегов input, img, ol|ul. На вход принимает:
    :param tag_list: список тегов, по которым нужно провести анализ
    :param html_data: html-код для анализа"""

    tags_dict = dict()

    for tag_dict in tag_list:
        if 'ul' in tag_dict.keys() or 'ol' in tag_dict.keys():
            lists_dict = dict()

            for key, value in tag_dict.items():
                with_li, wo_li = 0, 0
                uls_ols = html_data.findAll(key)

                for list_data in uls_ols:
                    # так как li может в части слова, то "уточняем" тег
                    if f'<{value}' in str(list_data):
                        with_li += 1
                    else:
                        wo_li += 1

                lists_dict[key] = {'with li': with_li, 'without li': wo_li, f'total {key}': len(html_data.findAll(key))}
            tags_dict.update(lists=lists_dict)

        elif 'input' in tag_dict.keys():

            for tag, attrs in tag_dict.items():
                input_dict = dict()
                attr_dict = {attr: {'Empty': 0, 'With value': 0, 'Not found': 0} for attr in attrs}
                tags_data = list(html_data.select(f'{tag}'))

                for list_part in tags_data:
                    list_part = str(list_part).lstrip('<').rstrip('/>').split()
                    del list_part[list_part.index('input')]
                    list_part = {i.split('=')[0].strip("'"): i.split('=')[1].strip('"') for i in list_part if '=' in i}

                    for attr in attrs:
                        if attr in list_part.keys() and len(list_part[attr]) != 0:
                            attr_dict[attr]['With value'] += 1
                        elif attr in list_part.keys() and len(list_part[attr]) == 0:
                            attr_dict[attr]['Empty'] += 1
                        elif attr not in list_part.keys():
                            attr_dict[attr]['Not found'] += 1

                input_dict.update(total=len(tags_data))
            # объединяем словари после работы основого цикла
            input_dict |= attr_dict
            tags_dict.update(input=input_dict)

        elif 'img' in tag_dict.keys():
            imgs_dict = {value: {'Empty': 0, 'With value': 0, 'Not found': 0}
                         for values in tag_dict.values() for value in values}
            imgs_data_alt = html_data.find_all('img', alt=True)
            imgs_data_alt_noalt = html_data.find_all('img', alt=False)

            imgs_dict['alt']['Not found'] += len(imgs_data_alt_noalt)

            for tag in imgs_data_alt:
                for attr in imgs_dict.keys():
                    if tag.has_attr(attr):
                        if len(tag.attrs[attr]) != 0:
                            imgs_dict[attr]['With value'] += 1
                        elif len(tag[attr]) == 0:
                            imgs_dict[attr]['Empty'] += 1
                    else:
                        imgs_dict[attr]['Not found'] += 1
            else:
                tags_dict.update(img = imgs_dict)
                tags_dict['img']['total'] = len(imgs_data_alt) + len(imgs_data_alt_noalt)

    return tags_dict