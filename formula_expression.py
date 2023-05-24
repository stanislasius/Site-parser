from rich.console import  Console

rich_console = Console().print


def formula(json_result):
    single_tag_points = 0.0
    multi_tag_points = 0.0
    multi_tag_attr_points = 0.0
    em_count = int(json_result.get('em').get('total')) if type(json_result.get('em')) is dict else 0
    strong_count = int(json_result.get('strong').get('total')) if type(json_result.get('strong')) is dict else 0
    h1_count = int(json_result.get('h1').get('total')) if type(json_result.get('h1')) is dict else 0
    img_count = json_result.get('img').get('total')
    input_count = json_result.get('input').get('total')

    em_count = int(json_result.get('em').get('total')) if type(json_result.get('em')) is dict else 0
    strong_count = int(json_result.get('strong').get('total')) if type(json_result.get('strong')) is dict else 0
    h1_count = int(json_result.get('h1').get('total')) if type(json_result.get('h1')) is dict else 0
    img_count = json_result.get('img').get('total')
    input_count = json_result.get('input').get('total')

    for key_main in json_result:
        if type(json_result.get(key_main)) is bool and key_main in ('header', 'nav', 'main', 'footer',
                                                             'section', 'article', 'strong', 'em', 'h1'):
            single_tag_points += 0.3 if json_result.get(key_main) else 0
            single_tag_points = round(single_tag_points, 3)

        elif type(json_result.get(key_main)) is dict and key_main in ('em', 'strong', 'h1'):
            if key_main != 'h1':
                multi_tag_points += 0.3 * int(json_result.get(key_main).get('total'))
                multi_tag_points = round(multi_tag_points, 4)

            else:
                multi_tag_points += 0.3 if int(json_result.get('h1').get('total')) == 1 else \
                    0.2 * (1 - int(json_result.get('h1').get('total')))
                multi_tag_points = round(multi_tag_points, 4)

        elif type(json_result.get(key_main)) is dict and key_main in ('img', 'input'):
            match key_main:
                case 'input':
                    for subkey_input_attr, subvalue_input_attr in json_result.get(key_main).items():
                        match subkey_input_attr:
                            case 'name':
                                multi_tag_attr_points += 0.3 * subvalue_input_attr.get('With value') \
                                    if subvalue_input_attr.get('With value') >= 1 else 0

                                multi_tag_attr_points -= 0.1 * subvalue_input_attr.get('Not found') \
                                    if subvalue_input_attr.get('Not found') == 1 else 0

                                multi_tag_attr_points = round(multi_tag_attr_points, 4)
                            case 'placeholder':
                                multi_tag_attr_points += 0.2 * subvalue_input_attr.get('With value') \
                                    if subvalue_input_attr.get('With value') >= 1 else 0

                                multi_tag_attr_points = round(multi_tag_attr_points, 4)
                case 'img':
                    for subkey_input_attr, subvalue_input_attr in json_result.get(key_main).items():
                        match subkey_input_attr:
                            case 'alt':
                                multi_tag_attr_points += 0.3 * subvalue_input_attr.get('With value') \
                                    if subvalue_input_attr.get('With value') >= 1 else 0

                                multi_tag_attr_points -= 0.2 * subvalue_input_attr.get('Not found') \
                                    if subvalue_input_attr.get('Not found') >= 1 else 0

                                multi_tag_attr_points -= 0.2 * subvalue_input_attr.get('Empty') \
                                    if subvalue_input_attr.get('Empty') >= 1 else 0

                                multi_tag_attr_points = round(multi_tag_attr_points, 4)
                            case 'title':
                                multi_tag_attr_points += 0.1 * subvalue_input_attr.get('With value') \
                                    if subvalue_input_attr.get('With value') >= 1 else 0

                                multi_tag_attr_points = round(multi_tag_attr_points, 4)

    max_points = round(1.8 + (em_count * 0.2) + (strong_count * 0.2) +
                        ((h1_count + 1 - h1_count) * 0.2) + (img_count * 0.5) + (input_count * 0.5), 1)
    estimated_points = round(single_tag_points + multi_tag_points + multi_tag_attr_points, 1)

    rich_console(f'Баллов набрано: {estimated_points} из {max_points}', style='yellow')
    rich_console(f'Сайт соответствует рассматриваемым требованиям на [red]'
                 f'{round((estimated_points / max_points) * 100, 1)}%[/red]', style='yellow')

    return


