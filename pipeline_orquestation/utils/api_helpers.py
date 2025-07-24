import requests

def fetch_data(url):
    return requests.get(url).json()
