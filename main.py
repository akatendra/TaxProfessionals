import aiohttp
import asyncio
import time

# Set up logging
import logging.config

import request
import scraper
import xlsx

"""fix yelling at me error"""
# Monkey Patch:
# https://pythonalgos.com/runtimeerror-event-loop-is-closed-asyncio-fix/
from functools import wraps

from asyncio.proactor_events import _ProactorBasePipeTransport


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
    _ProactorBasePipeTransport.__del__)
"""fix yelling at me error end"""

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def spent_time():
    global start_time
    sec_all = time.time() - start_time
    if sec_all > 60:
        minutes = sec_all // 60
        sec = sec_all % 60
        time_str = f'| {int(minutes)} min {round(sec, 1)} sec'
    else:
        time_str = f'| {round(sec_all, 1)} sec'
    start_time = time.time()
    return time_str


def get_html(url):
    html = request.get_request(url)
    html = scraper.prettify_html(html)
    return html


################################### asyncio ###################################
async def fetch_personal_links(session, url):
    try:
        async with session.get(url) as response:
            logger.debug(f'url: {url}')
            logger.debug(f'Status: {response.status}')
            logger.debug(
                f'Content-type: {response.headers["content-type"]}')
            html = await response.text()
            scraper.parse_personal_links(html)
    except Exception as error:
        logger.debug(f'{str(error)}')


async def main_personal_links():
    tasks = []

    # Start sessions
    async with aiohttp.ClientSession(headers=request.HEADERS) as session:
        url_blacktaxprofessionals = 'https://blacktaxprofessionals.com/taxprofessionals/category/taxprofessionals/page/'
        for i in range(53):
            url_cat = url_blacktaxprofessionals + str(i) + '/'
            logger.debug(f'url_cat: {url_cat}')
            tasks.append(fetch_personal_links(session, url_cat))
        personal_links_raw = await asyncio.gather(*tasks)
    return personal_links_raw


###############################################################################


################################### asyncio ###################################

def get_personal_links():
    url_blacktaxprofessionals = 'https://blacktaxprofessionals.com/taxprofessionals/category/taxprofessionals/page/'
    for i in range(53):
        url_cat = url_blacktaxprofessionals + str(i) + '/'
        logger.debug(f'url_cat: {url_cat}')
        html = get_html(url_cat)
        # logger.debug(f'html: {html}')
        scraper.parse_personal_links(html)
    return scraper.save_personal_links()


def get_personal_info(url):
    html = get_html(url)
    return html


if __name__ == '__main__':
    #####################################
    # get personal links by requests
    #####################################
    # Медленнее чем asyncio, но стабильнее. Но результат от раза к разу тоже
    # почему-то отличается. Почему?
    #####################################
    # time_begin = start_time = time.time()
    # get_personal_links()
    # logger.debug(f'{spent_time()}')
    #####################################

    #####################################
    # get personal links by a asyncio
    #####################################
    # Нестабильный выходной результат. Количество ссылок пляшет от запуска к
    # запуску. Такое ощущение, что запросы идут так быстро, что сервер
    # перегружается, возникает 500 ошибка и парсинг некоторых или всех страниц
    # не приносит результата. Как итог - меньше ссылок, чем есть на странице.
    #####################################
    # time_begin = start_time = time.time()
    # asyncio.run(main_personal_links())
    # personal_links = scraper.save_personal_links()
    # logger.debug(f'personal_links: {len(personal_links)} | {personal_links}')
    # logger.debug(f'{spent_time()}')
    #####################################

    # Read personal links from file
    with open('personal_links.txt', 'r') as file:
        personal_links = []
        for line in file.readlines():
            personal_links.append(line.replace('\n', ''))
    logger.debug(f'personal_links: {len(personal_links)} | {personal_links}')

    # url_test = 'https://blacktaxprofessionals.com/taxprofessionals/rise-tax-service/'
    # url_test = 'https://blacktaxprofessionals.com/taxprofessionals/tax-queen-services/'
    time_begin = start_time = time.time()

    for link in personal_links:
        scraper.parse_person(link, get_personal_info(link))

    xlsx.hyperlink_style('tax_professionals.xlsx')

    spent_time()
