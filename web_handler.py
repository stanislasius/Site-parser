from requests import head as requests_head
from rich.console import Console

rich_console = Console().print


def check_site(site):
    """Проверка доступности Caffesta Beanstalk"""

    rich_console(f'Проверка доступности {site}', style = 'bold red')

    try:
        status = requests_head(site).status_code
    except ConnectionError as UnexpecetedErr:
        rich_console(f'Непредвиденная проблема подключения: {UnexpecetedErr}')
    else:
        match status:
            case 200:
                return True
            case 401:
                return True
            case _:
                rich_console(f"""[bold]Невозможно получить доступ к {site} из-за ошибки {status}[/bold]""",
                             style = 'yellow')
                return False

