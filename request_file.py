

import pickle
import urllib.request
import requests
from os.path import join,isfile
from os import listdir
import urllib

def counter_for_files(path):
    
    """Подсчет файлов в директории"""
        
    onlyfiles = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles



def request_func(ID):
    if f'dump\\{ID}.ttl' in counter_for_files('dump'):
        return None
    with requests.get(f"https://www.wikidata.org/wiki/Special:EntityData/{ID}.ttl", 
                      stream=True, proxies=urllib.request.getproxies()) as r:
        if r.status_code != 200:
            with open(f"Logging.txt", "a" , encoding='utf-8') as file:
                file.write(f'{ID} :  {r.status_code}\n')
            return None
        with open(f"dump//{ID}.ttl", "w" , encoding='utf-8') as file:
            file.write(r.text)
        return None
