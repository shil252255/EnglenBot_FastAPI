import asyncio
import json
import string
import time

import aiohttp
import requests
from bs4 import BeautifulSoup, SoupStrainer, Tag

BASE_URL = 'https://www.babla.ru/английский-русский'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}


def dump_data_to_json(file_name: str, data: list | dict) -> None:
    """
    Save data to json file.
    """
    with open(f'files/{file_name}.json', 'w') as file:
        json.dump(data, file)


def get_word_list_soup(char: str, page_num: int = 1) -> BeautifulSoup:
    """
    Return BeautifulSoup for word list page by char (a-z) and page number.
    """
    url = f'{BASE_URL}/{char}/{page_num}'
    return BeautifulSoup(requests.get(url=url, headers=HEADERS).content, features="lxml")


def filter_valid_word(tag: Tag) -> bool:
    """
    Возвращает True только для ссылок на страницы слов, а не фраз, аббревиатур или имен собственных.
    """
    return (tag and
            tag.has_attr('href') and
            len(tag.text.split()) == 2 and
            tag.text.split()[1].islower())


def get_last_page_num(char: str) -> int:
    """
    Получаем значение ссылки на последнюю страницу списка из пагинатора и оттуда получаем номер страницы,
    если ссылки нет значит страница единственная возвращаем 1.
    """
    soup = get_word_list_soup(char, 1).find_all("a", "dict-pag-button")
    return int(soup[-1]['href'].split('/')[-1]) if soup else 1


def get_links_from_soup(soup: BeautifulSoup) -> set:
    """
    Получаем со странницы все ссылки на страницы подходящих слов, сразу избавляясь от повторов.
    """
    div = soup.find("div", "dict-select-wrapper").findAll(filter_valid_word)
    return set(['https:' + str(a['href']) for a in div])


def get_words_links_set() -> set:
    """
    Возвращает все ссылки на все страницы слов, которые доступны на сайте.
    """
    link_set = set()
    for char in string.ascii_lowercase:
        for page_num in range(1, get_last_page_num(char) + 1):
            link_set |= get_links_from_soup(get_word_list_soup(char, page_num))
    return link_set


def get_and_save_words_page_links():
    """
    Загружает все ссылки на страницы слов и сохраняет их в файл.
    """
    links_set = get_words_links_set()
    dump_data_to_json('links', list(links_set))


async def get_soup(session: aiohttp.ClientSession, link: str) -> Tag:
    async with session.get('https:' + link) as resp:
        text = await resp.read()
    soup_filter = SoupStrainer('div', {'class': 'quick-results container'})
    return BeautifulSoup(text, features="lxml", parse_only=soup_filter).div


def get_word_from_div(div: Tag) -> dict:
    return {
        'word': div.find('a', 'babQuickResult').text,
        'translations': ', '.join([a.text for a in div.findAll('a', {"title": True})]),
        'suffixes': [span.text for span in div.findAll('span', 'suffix')]
    }


def get_child_div_classes(tag: Tag) -> list:
    return [div.get('class') for div in tag.findAll('div', recursive=False)]


def filter_quick_result_entry_tags(tag: Tag) -> bool:
    child_div_classes = get_child_div_classes(tag)
    return (
            tag and
            "quick-result-entry" in tag.get('class', []) and
            ['quick-result-option'] in child_div_classes and
            ['quick-result-overview'] in child_div_classes
    )


def get_words_from_soup(soup: Tag) -> list:
    return [*map(get_word_from_div, soup.findAll(filter_quick_result_entry_tags, recursive=False)[:3])]


async def get_words_from_link(session: aiohttp.ClientSession, link: str) -> list:
    soup = await get_soup(session, link)
    return get_words_from_soup(soup)


async def get_all_words_from_links(links_list: list | set) -> list:
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [asyncio.ensure_future(get_words_from_link(session, link)) for link in links_list]
        res = await asyncio.gather(*tasks)
    return [item for i in res for item in i]


async def save_part_of_words(links_list: list | set, set_size: int, start_index: int):
    t = time.time()
    words_list = await get_all_words_from_links(links_list[start_index:start_index + set_size])
    print(f'{time.time() - t} seconds for {start_index} - {start_index + set_size} links set.')
    dump_data_to_json(f'words {start_index/set_size}', words_list)


def load_links_from_file():
    with open('links.json', 'r') as file:
        links = json.load(file)
    links.sort()
    return links


def get_and_save_words():
    words_pages_links = load_links_from_file()
    print(len(words_pages_links))
    links_set_size = 1000
    for n in range(0, len(words_pages_links), links_set_size):
        asyncio.run(save_part_of_words(words_pages_links, links_set_size, n))


if __name__ == '__main__':
    pass


