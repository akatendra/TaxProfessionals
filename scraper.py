from datetime import timedelta, datetime

import os

import xlsx

from bs4 import BeautifulSoup

# Set up logging
import logging.config

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

personal_links_list = []


def prettify_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.prettify()


def parse_personal_links(data):
    global personal_links_list
    soup = BeautifulSoup(data, 'lxml')
    items = soup.select('a[title*="View:"]')
    # logger.debug(f'items: {items}')
    for item in items:
        personal_links_list.append(item['href'])
    logger.debug('###############################################')
    logger.debug(
        f'Number of items founded on page: {len(items)}')
    logger.debug('###############################################')


def remove_file(file):
    if os.path.isfile(file):
        # os.remove() function to remove the file
        os.remove(file)
        # Printing the confirmation message of deletion
        print("File Deleted successfully")
    else:
        print("File does not exist")


def save_personal_links():
    remove_file('personal_links_list.txt')
    logger.debug(
        f'personal_links_list: {len(personal_links_list)} |  {personal_links_list}')
    with open('personal_links_list.txt', 'a') as file:
        for link in personal_links_list:
            file.write(link + '\n')

    remove_file('personal_links.txt')
    personal_links = set(personal_links_list)
    logger.debug(
        f'personal_links set: {len(personal_links)} | {personal_links}')
    with open('personal_links.txt', 'a') as file:
        for link in personal_links:
            file.write(link + '\n')
    return personal_links


def parse_person(url, data):
    soup = BeautifulSoup(data, 'lxml')
    title = soup.select_one('h1').text.strip()
    logger.debug(f'title: {title}')

    image = soup.select_one('span[class*="embed-responsive"] img')
    if image:
        image_url = image['src']
    else:
        image_url = None
    logger.debug(f'image_url: {image_url}')

    description = soup.select_one('div[class*="geodir-field-post_content"]')
    if description:
        description = description.text.strip()
    logger.debug(f'description: {description}')

    email = soup.select_one('div[class*="geodir-field-email"] a')
    if email:
        email = email.text.strip().replace('\r', '').replace('\n', '').replace(
            ' ', '')
    logger.debug(f'email: {email}')

    phone = soup.select_one('div[class*="geodir-field-phone"] a')
    if phone:
        phone = phone.text.strip()
    logger.debug(f'phone: {phone}')

    website = soup.select_one('div[class*="geodir-field-website"] a')
    if website:
        website = website.text.strip()
    logger.debug(f'website: {website}')

    instagram = soup.select_one('div[class*="geodir-field-instagram"] a')
    if instagram:
        instagram = instagram['href']
        if instagram == 'https://www.instagram.com/':
            instagram = None
    logger.debug(f'instagram: {instagram}')

    facebook = soup.select_one('div[class*="geodir-field-facebook"] a')
    if facebook:
        facebook = facebook['href']
        if facebook == 'https://www.facebook.com/':
            facebook = None
    logger.debug(f'facebook: {facebook}')

    address = soup.select_one('div[class*="geodir-field-address"]')
    if address:
        street_address = address.select_one(
            'span[itemprop="streetAddress"]')
        if street_address:
            street_address = street_address.text.strip()
        logger.debug(f'streetAddress: {street_address}')

        address_locality = address.select_one(
            'span[itemprop="addressLocality"]')
        if address_locality:
            address_locality = address_locality.text.strip()
        logger.debug(f'addressLocality: {address_locality}')

        address_region = address.select_one(
            'span[itemprop="addressRegion"]')
        if address_region:
            address_region = address_region.text.strip()
        logger.debug(f'addressRegion: {address_region}')

        postal_code = address.select_one('span[itemprop="postalCode"]')
        if postal_code:
            postal_code = postal_code.text.strip()
        logger.debug(f'postalCode: {postal_code}')

        data_out = {'personal_link': url,
                    'title': title,
                    'image_url': image_url,
                    'description': description,
                    'email': email,
                    'phone': phone,
                    'website': website,
                    'instagram': instagram,
                    'facebook': facebook,
                    'street_address': street_address,
                    'address_locality': address_locality,
                    'address_region': address_region,
                    'postal_code': postal_code
                    }
        logger.debug(f'data_out: {data_out}')

        xlsx.append_xlsx_file(data_out, 'tax_professionals.xlsx')




def reduce_white_spaces(string):
    string = string.replace('\n', '')
    while '  ' in string:
        string = string.replace('  ', ' ')
    return string


