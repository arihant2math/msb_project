import datetime
import time
from pathlib import Path

import click

from colorama import Fore

import requests


def get_media_url(chunklist_text):
    lines = chunklist_text.split("\n")
    for line in lines:
        if "media" in line:
            return line
    return None


@click.command()
@click.argument("base_url")
@click.argument("chunklist_file")
@click.option("--folder", default="out", help="Folder to save the files")
def download(base_url, chunklist_file, folder):
    # folder_name = "S101_at_Whipple_Av"
    # base_url = "http://wzmedia.dot.ca.gov/D4/S101_at_Whipple_Av.stream/"

    # Add trailing slash if not present
    if not base_url.endswith("/"):
        base_url += "/"

    # Create directory if it doesn't exist
    Path(folder).mkdir(parents=True, exist_ok=True)

    # get the real chunklist URL
    chunklist_url = base_url + chunklist_file
    last_url = ""

    # Main loop
    while True:
        try:
            # Gets the required media_url from the chunklist file
            resp = requests.get(chunklist_url)
            # Parses the file for the media URL, returns None if it can't find it
            media_url = get_media_url(resp.text)
            # Begins the log message
            print(f"{Fore.LIGHTBLUE_EX}[{media_url}]{Fore.RESET}", end=" ")
            # Downloads the media file if it's new and if it exists

            # If the parser couldn't find the media URL, it will return None
            if media_url is None:
                print(f"{Fore.LIGHTRED_EX}No media url found")
            # This means we're using the same media file as last iteration, so downloading is duplication
            elif last_url != media_url:
                resp = requests.get(base_url + media_url)
                file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".ts"
                with open(folder + "/" + file_name, "wb") as f:
                    f.write(resp.content)
                print(f"{Fore.LIGHTGREEN_EX}Downloaded as {file_name}")
            # This means that the media file is the same as the last iteration
            else:
                print(f"{Fore.LIGHTYELLOW_EX}No new media URL")
            last_url = media_url
            # Sleep for 4 seconds (it takes 7 seconds for the new media file to be set on the server)
            time.sleep(4)
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}ERROR {Fore.RED}" + str(e))
            time.sleep(4)


if __name__ == "__main__":
    download()
