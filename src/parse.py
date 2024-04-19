import requests
import json
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

from .load_html import get_page_html
from .data import domain, USER_AGENT


def get_soup_each_pages(link):
    full_link = f"{domain}{link}"
    req_link = requests.get(full_link, headers=USER_AGENT)
    return BeautifulSoup(req_link.content, "html.parser")


def get_data_from_link(link):
    soup_link = get_soup_each_pages(link)
    title = soup_link.find("span", {"data-id": "PageTitle"}).get_text(strip=True)
    full_address = soup_link.find("h2", {"class": "pt-1"}).get_text(strip=True)
    description = soup_link.find("div", {"itemprop": "description"})
    description_text = description.get_text(strip=True) if description else None
    price = soup_link.find("meta", {"itemprop": "price"}).get("content") if soup_link.find("meta", {"itemprop": "price"}) else None
    area = soup_link.find("div", {"class": "carac-value"}).get_text(strip=True)
    arr_images = soup_link.find("div", {"class": "primary-photo-container"})
    number_rooms = soup_link.find("div", {"class": "row teaser"}).get_text(strip=True)

    src_list = [img_tag.get("src") for img_tag in arr_images.find_all("img")] if arr_images else []

     
    # Split the address into separate parts
    address_parts = full_address.split(',')
    address = ','.join(address_parts[:-1]).strip()
    region = address_parts[-1].strip()

    return {
        "title": title,
        "address": address,
        "region": region,
        "description": description_text,
        "price": price,
        "area": area,
        "image_src": src_list,
        "number_rooms": number_rooms,
        "link": f"{domain}{link}"
    }


def parse_main_page():
    page = get_page_html()
    main_result = page.find_all("div", {"class": "row thumbnail-content"})
    links = [link.get('href') for result in main_result for link in result.find_all("a", {"class": "a-more-detail"})]
    link_data_list = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_data_from_link, link) for link in links]
        for future in futures:
            link_data_list.append(future.result())

    return link_data_list


def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)