from requests import head as requests_head


def check_site(site):

    print(f'Проверка доступности {site}')

    try:
        status = requests_head(site, allow_redirects=True).status_code
    except ConnectionError as UnexpectedErr:
        print(f'Непредвиденная проблема подключения: {UnexpectedErr}')
    else:
        match status:
            case 200:
                return True
            case _:
                print(f"Невозможно получить доступ к {site} из-за ошибки {status}")
                return check_site(site)
