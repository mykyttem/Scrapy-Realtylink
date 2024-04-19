from parse import parse_main_page, save_to_json

# TODO: all images src in arr 
# TODO: region
# TODO: parse 60  (now 20)


if __name__ == "__main__":
    data = parse_main_page()
    save_to_json(data, "links_data.json")