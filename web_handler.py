from requests import head as requests_head
from rich.console import Console

rich_console = Console().print

def check_site(site):

    rich_console(f'Проверка доступности {site}', style='yellow')

    try:
        status = requests_head(site, allow_redirects=True).status_code
    except ConnectionError as UnexpectedErr:
        rich_console(f'Непредвиденная проблема подключения: {UnexpectedErr}', style='red')
    else:
        match status:
            case 200:
                return True
            case _:
                rich_console(f"Невозможно получить доступ к {site} из-за ошибки {status}", style='red')
                return check_site(site)
