import os
from pathlib import Path

from requests import request
from dotenv import load_dotenv

load_dotenv()

SUB_INFO_URL = "https://api.opensubtitles.com/api/v1/subtitles"
DL_SUB_URL = "https://api.opensubtitles.com/api/v1/download"
SUB_DIR = Path('SubsParser/Subs')

HEADERS = {
    "Content-Type": "application/json",
    "Api-Key": os.environ['OPENSUBTITLES_TOKEN']
}
SUB_SEARCH_PARAMS = {
        'languages': 'en',
        'order_by': 'download_count',
    }


def request_first_sub_file_info(sub_params: dict) -> dict | None:
    response = request(method="GET", url=SUB_INFO_URL, headers=HEADERS, params=sub_params)
    response.raise_for_status()
    response_dict = (response.json())
    if response_dict.get('total_count'):
        return response_dict['data'][0]['attributes']['files'][0]


def request_dnl_link(sub_file_info: dict) -> dict:
    response = request(method="POST", url=DL_SUB_URL, headers=HEADERS, params=sub_file_info)
    response.raise_for_status()
    return response.json()['link']


def download_sub(link, file):
    response = request('GET', link)
    response.raise_for_status()
    SUB_DIR.mkdir(parents=True, exist_ok=True)
    with open(file, 'wb') as f:
        f.write(response.content)
    return 1
    # TODO А тут прям надо логирование и проверка на наличие файла


def download(params: dict) -> dict:
    sub_file_name = f'{params["imdb_id"]}'
    if params.get("season_number"):
        sub_file_name += f'_S{params["season_number"]:02.0f}E{params["episode_number"]:02.0f}.srt'
    most_popular_sub_file_info = request_first_sub_file_info(params)
    if most_popular_sub_file_info:
        dnl_link = request_dnl_link(most_popular_sub_file_info)
        return download_sub(dnl_link, SUB_DIR / sub_file_name)


def download_sub_for_serial(title_imdb_id):
    params = SUB_SEARCH_PARAMS.copy()
    params['imdb_id'] = title_imdb_id
    if not download(params):
        params['season_number'] = 1
        params['episode_number'] = 1
        while True:
            if download(params):
                params['episode_number'] += 1
            elif params['episode_number'] > 1:
                params['season_number'] += 1
                params['episode_number'] = 1
            else:
                break


if __name__ == '__main__':
    download_sub_for_serial(title_imdb_id='tt1190634')  # Просто пример (сериал "пацаны")
    # TODO надо бы тут использовать сессии а не вот это вот все каждый раз
