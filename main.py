import time
from src.parse import parse_main_page, save_to_json


# TODO: all images src in arr 
# TODO: 60


if __name__ == "__main__":
    start_time = time.time()

    data = parse_main_page()
    save_to_json(data, "links_data.json")

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: {:.2f} seconds".format(execution_time))