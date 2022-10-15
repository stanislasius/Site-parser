import requests
import bs4


url = "https://caffesta.com/ru/help/109"
response = requests.get(url)
data = bs4.BeautifulSoup(response.text, 'html5lib')
tag_dict_count = dict()
