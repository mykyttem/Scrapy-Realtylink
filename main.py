from parse import parse_main_page, save_to_json

# TODO: all images src in arr 
# TODO: region
# TODO: parse 60  (now 20)


domain = "https://realtylink.org"
url = "/en/properties~for-rent?uc=1"
full_url = f"{domain}{url}"

if __name__ == "__main__":
    data = parse_main_page(full_url)
    save_to_json(data, "links_data.json")