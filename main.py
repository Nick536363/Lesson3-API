import requests
import os
from urllib.parse import urlparse
import argparse
from dotenv import load_dotenv 



def get_short_link(long_url, token):
    url = "https://api.vk.com/method/utils.getShortLink"
    
    params = {
        "url": long_url,
        "access_token": token,
        "v": "5.199",    
    }

    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(url, params=params, headers=headers)
    response.raise_for_status()

    return response.json()['response']['short_url']


def count_clicks(token, short_link):
    url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "key": short_link,
        "interval": "day",
        "v": "5.236",
        "extended": 0,
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()['response']['stats']

def main():
    load_dotenv()
    token = os.getenv('TOKEN')
    parser = argparse.ArgumentParser(description='Сокращает ссылки и выводит количество переходов по ней')
    parser.add_argument('--link', help='Введите ссылку:')
    args = parser.parse_args()
    long_url = args.link
    parsed_url = urlparse(long_url)
    try:   
        if parsed_url.netloc == 'vk.cc':
            print("Кол-во кликов по ссылке:", 
                count_clicks(token, parsed_url.path[1:])[0]["views"])
        else: 
            print(f"Короткая ссылка: {get_short_link(long_url, token)}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")


if __name__ == "__main__":
    main()