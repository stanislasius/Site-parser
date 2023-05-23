import rich.box
from rich.table import Table
from rich.console import Console

rich_console = Console().print


def create_table_single_tag(data):
    table = Table(  rich.table.Column(header="[yellow]Теги, которые есть на сайте[/yellow]", justify='center'),
                    rich.table.Column(header="[yellow]Теги, которых нет на сайте[/yellow]", justify='center'),
                    title='[magenta bold]Анализ сайта на наличие определённых тегов[/magenta bold]',
                    show_lines=True,
                    expand=False,
                    box=rich.box.SQUARE_DOUBLE_HEAD,
                    title_justify='center'
                    )

    has_tags, hasnt_tags = list(), list()
    for key, value in data.items():
        if type(value) is bool:
            if str(value) == 'False':
                hasnt_tags.append(key)
            elif str(value) == 'True':
                has_tags.append(key)
    else:
        table.add_row(f"[green]{', '.join(has_tags)}[/green]", f"[red]{', '.join(hasnt_tags)}[red]")
        rich_console(table)

    return


def create_table_multi_tag(data):
    table = Table(  rich.table.Column(header="[yellow]Теги[/yellow]", justify='center'),
                    rich.table.Column(header="[yellow]Количество на сайте[/yellow]", justify='center'),
                    rich.table.Column(header="[yellow]Текст в тегах[/yellow]", justify='center'),
                    title='[magenta bold]Количество некоторых тегов[/magenta bold]',
                    show_lines=True,
                    expand=False,
                    box=rich.box.SQUARE_DOUBLE_HEAD,
                    title_justify='center'
                    )

    for key, value in data.items():
        if type(value) is dict and key in ('em', 'strong', 'h1'):
            table.add_row(f'[#34D1B2]{key}[/#34D1B2]', f'[#34D1B2]{value.get("total")}[#34D1B2]', f'[#34D1B2]{value.get("Текст")}[#34D1B2]')
    else:
        rich_console(table)

    return


def create_table_tag_attr_multi(data):
    table = Table(  rich.table.Column(header="[yellow]Тег[/yellow]", justify='center'),
                    rich.table.Column(header="[yellow]Всего тегов[/yellow]", justify='center'),
                    rich.table.Column(header="[yellow]Аттрибуты тега и их количество[/yellow]", justify='center'),
                    title='[magenta bold]Количество аттрибутов определённого тега[/magenta bold]',
                    show_lines=True,
                    expand=False,
                    box=rich.box.SQUARE_DOUBLE_HEAD,
                    title_justify='center'
                    )

    for key, value in data.items():
        if key == 'img':
            table.add_row(
                f"[#34D1B2]{key}[/#34D1B2]",
                f"[blue]{data.get(key).get('total')}[/blue]",
                f"[#34D1B2]alt[/#34D1B2]: [red]Нет значения - {data.get(key).get('alt').get('Not found')}[/red], "
                    f"[yellow]Пустое значение - {data.get(key).get('alt').get('Empty')}[/yellow], "
                    f"[green]Есть значение  - {data.get(key).get('alt').get('With value')}\n[/green]"
                
                f"[#34D1B2]title[/#34D1B2]: [red]Нет значения - {data.get(key).get('title').get('Not found')}[/red], "
                    f"[yellow]Пустое значение - {data.get(key).get('title').get('Empty')}[/yellow], "
                    f"[green]Есть значение  - {data.get(key).get('title').get('With value')}[/green]")

        elif key == 'input':
            table.add_row(
                f"[#34D1B2]{key}[/#34D1B2]",
                f"[blue]{data.get(key).get('total')}[/blue]",
                f"[#34D1B2]name[/#34D1B2]: [red]Нет значения - {data.get(key).get('name').get('Not found')}[/red], "
                    f"[yellow]Пустое значение - {data.get(key).get('name').get('Empty')}[/yellow], "
                    f"[green]Есть значение  - {data.get(key).get('name').get('With value')}[/green]\n"
                
                f"[#34D1B2]id[/#34D1B2]: [red]Нет значения - {data.get(key).get('id').get('Not found')}[/red], "
                    f"[yellow]Пустое значение - {data.get(key).get('id').get('Empty')}[/yellow], "
                    f"[green]Есть значение  - {data.get(key).get('id').get('With value')}[/green]\n"
                
                f"[#34D1B2]type[/#34D1B2]: [red]Нет значения - {data.get(key).get('type').get('Not found')}[/red], "
                    f"[yellow]Пустое значение - {data.get(key).get('type').get('Empty')}[/yellow], "
                    f"[green]Есть значение  - {data.get(key).get('type').get('With value')}[/green]\n"
                
                f"[#34D1B2]value[/#34D1B2]: [red]Нет значения - {data.get(key).get('value').get('Not found')}[/red], "
                    f"[yellow]Пустое значение - {data.get(key).get('value').get('Empty')}[/yellow], "
                    f"[green]Есть значение  - {data.get(key).get('value').get('With value')}[/green]")

    rich_console(table)

    return

