
import requests
from bs4 import BeautifulSoup

# Отправляем HTTP-запрос
url = 'https://zakupki.gov.ru/epz/order/notice/notice223/common-info.html?noticeInfoId=16031756'
response = requests.get(url)

# Проверяем успешность запроса
if response.status_code == 200:
    # Используем BeautifulSoup для парсинга страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Пример: извлечение заголовков h1 на странице
    headings = soup.find_all('h1')
    for heading in headings:
        print(heading.text)
else:
    print('Ошибка при запросе:', response.status_code)
