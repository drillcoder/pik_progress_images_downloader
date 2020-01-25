import requests
import os
import sys
from datetime import date

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/13.0.3 Safari/605.1.15'
}

base_folder = os.path.abspath(os.path.dirname(sys.argv[0]))+'/Ход строительства/'
os.system('clear')
bulk_id = input('Введите цифры из адреса хода строительства.\r\n'
                'Например 4053 из https://www.pik.ru/sp/progress/4053\r\n'
                'Что соответствует проекту Саларьево Парк корпус 18.1: ')
if bulk_id == '':
    print('Пустой номер')
    sys.exit()
base_url = f'https://api.pik.ru/v1/news?bulk_id={bulk_id}&limit=all&is_content=1&is_progress=1'

session = requests.Session()
request = session.get(base_url, headers=headers)
if request.status_code == requests.codes.ok:
    if request.json().get('message') == 'ERR_NEWS_NOT_FOUND':
        print('Неверный номер')
        sys.exit()
    for item in request.json().get('items'):
        public_date = date.fromtimestamp(int(item['public_date']))
        gallery = item['gallery']
        gallery.append({'file_path': item['preview']})
        folder = base_folder + public_date.strftime('%Y.%m.%d')
        if not os.path.exists(folder):
            os.makedirs(folder)
        for image in gallery:
            image_url = 'https:' + image['file_path']
            request = session.get(image_url, headers=headers, stream=True)
            if request.status_code == requests.codes.ok:
                file_name = image['file_path'].split('/')[-1]
                out = open(folder + '/' + file_name, 'wb')
                out.write(request.content)
                out.close()
            else:
                print('Ошибка =( Попробуйте перезапустить')
                sys.exit()
else:
    print('Ошибка =( Попробуйте перезапустить')
