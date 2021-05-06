import requests
import json
import datetime as dt
import os
from pathlib import Path


def kanye_downloader():
    r = requests.get("https://api.kanye.rest/").json()
    json_object = json.dumps(r, indent=4)
    now = dt.datetime.now()
    file_directory = make_directory(now)
    file_name = f'kanye_quote_{now.strftime("%Y_%m_%d_%H_%M_%S")}.json'
    with open(f"{file_directory}/{file_name}", "w") as outfile:
        outfile.write(json_object)
    return


def make_directory(now):
    time_dir_name = now.strftime("%Y/%m/%d/%H/%M")
    dir_name = f"./kanye_quote_data/{time_dir_name}"
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    return dir_name


if __name__ == "__main__":
    kanye_downloader()
