import time
import json
from src.parse import parse_main_page, save_to_json


# TODO: all images src in arr 


def count_objects_in_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        count = len(data)
    return count


if __name__ == "__main__":
    start_time = time.time()

    data = parse_main_page()
    save_to_json(data, "links_data.json")

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: {:.2f} seconds".format(execution_time))

    # counting the number of objects in the links_data.json file
    objects_count = count_objects_in_json("links_data.json")
    print(f"numbers of objects: {objects_count}")