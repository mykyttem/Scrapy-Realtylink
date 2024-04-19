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


def get_text_strip(element):
    return element.get_text(strip=True) if element else None


def find_element(soup, selector, attrs=None):
    return soup.find(selector, attrs)


def get_data_from_link(link):
    soup_link = get_soup_each_pages(link)

    # Helper function to simplify finding all elements
    def find_all(element, selector, attrs=None):
        return element.find_all(selector, attrs)

    # Helper function to simplify element finding
    def find(selector, attrs=None):
        return find_element(soup_link, selector, attrs)

    # Extract data from the page
    title = get_text_strip(find("span", {"data-id": "PageTitle"}))
    full_address = get_text_strip(find("h2", {"class": "pt-1"}))
    description_text = get_text_strip(find("div", {"itemprop": "description"}))
    price = find("meta", {"itemprop": "price"}).get("content") if find("meta", {"itemprop": "price"}) else None
    area = get_text_strip(find("div", {"class": "carac-value"}))
    arr_images = find("div", {"class": "primary-photo-container"})
    number_rooms = get_text_strip(find("div", {"class": "row teaser"}))

    # Extract image sources
    src_list = [img_tag.get("src") for img_tag in find_all(arr_images, "img")] if arr_images else []

    # Split the full address into separate parts
    address_parts = full_address.split(',')
    address = ','.join(address_parts[:-1]).strip()
    region = address_parts[-1].strip()

    # Extract price history
    price_history_table = find("table", {"class": "table-striped"})
    if price_history_table:
        rows = find_all(price_history_table, "tr")  # Corrected the line here
        price_history = []
        for row in rows[1:]:
            cols = find_all(row, "td")  # Corrected the line here
            date = get_text_strip(cols[0]) 
            status = get_text_strip(cols[1])
            price = get_text_strip(cols[2])
            price_history.append({"date": date, "status": status, "price": price})
    else:
        price_history = None

    # Construct the data dictionary
    return {
        "title": title,
        "address": address,
        "region": region,
        "description": description_text,
        "price": price,
        "area": area,
        "image_src": src_list,
        "number_rooms": number_rooms,
        "date": price_history,
        "link": f"{domain}{link}"
    }


def parse_main_page():
    """
        Parse the main page to retrieve links and extract data from property pages.
    """
    page = get_page_html()
    main_result = page.find_all("div", {"class": "row thumbnail-content"})
    links = [link.get('href') for result in main_result for link in result.find_all("a", {"class": "a-more-detail"})]
    link_data_list = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_data_from_link, link) for link in links]
        for future in futures:
            data = future.result()

            if data not in link_data_list:
                link_data_list.append(data)

    return link_data_list


def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)