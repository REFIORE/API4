import requests
import os
from urllib.parse import urlparse, unquote
from datetime import datetime
from dotenv import load_dotenv


def download_images(url, filepath, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    os.makedirs("images", exist_ok=True)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    response = requests.get(url)
    links=response.json()['links']['flickr']['original']

    for number, link in enumerate(links):
        download(link, f'images/spacex{number}.jpg')


def get_extention_file(url):
    decoded_url=unquote(url)
    parsed_url=urlparse(decoded_url)
    path, fullname=os.path.split(parsed_url.path)
    filename, extention=os.path.splitext(fullname)
    return filename, extention


def get_apod_images():
    count=30
    payload = {'api_key':os.environ['NASA_TOKEN'], 'count': count}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=payload)
    links=response.json()
    for link in links:
        if link.get('media_type')=='image':
            if link.get('hdurl'):
                nasa_image=link['hdurl'] or link['url']
            filename, extention=get_extention_file(nasa_image)
            path = os.path.join('images', f'{filename}{extention}')
            download(nasa_image, path)


def get_epic_image():
    count=5
    payload = {'api_key':os.environ['NASA_TOKEN'], 'count': count}
    response = requests.get('https://api.nasa.gov/EPIC/api/natural', params=payload)
    images=response.json()
    for image in images:
        date=image['date']
        name=image['image']
        date_image = datetime.fromisoformat(date).strftime("%Y/%m/%d")
        link=f'https://api.nasa.gov/EPIC/archive/natural/{date_image}/png/{name}.png'
        download(link, f'images/{name}.png', payload)

def main():
    load_dotenv()
    fetch_spacex_last_launch()
    get_apod_images()
    get_epic_image()


if __name__ == '__main__':
    main()