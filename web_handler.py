from requests import exceptions
from requests import head as requests_head
import verifications

from rich.console import Console

rich_console = Console().print


def check_site(site):

    rich_console(f'Проверка доступности {site}', style='yellow')

    try:
        status = requests_head(site, allow_redirects=True).status_code
    except exceptions.ConnectionError as UnexpectedErr:
        rich_console(f'Непредвиденная проблема подключения: {UnexpectedErr}', style='red')
        rich_console('Повторите ввод URL сайта: ', style='yellow')
        site = input()
        return check_site(verifications.check_site_address(site))
    else:
        match status:
            case 200:
                return site
            case _:
                rich_console(f"Невозможно получить доступ к {site} из-за ошибки {status}", style='red')
                return check_site(site)
