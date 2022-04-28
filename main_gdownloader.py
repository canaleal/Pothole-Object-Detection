
import gdown
import re
import sys
import os
import logging


def strip_link_from_raw_url(raw_url):
    result = re.search('https://drive.google.com/file/d/(.*)', raw_url)
    file_id = re.sub('/view\?usp=sharing', '', result.group(1))
    url = f'https://drive.google.com/uc?id={file_id}'
    return url

def download_google_file(raw_url, save_path):
    try:
        url = strip_link_from_raw_url(raw_url)    
        logging.info("Downloading starts...")
        gdown.download(url, save_path, quiet=False)
        
        return True
    except ValueError:
        logging.error(ValueError)
        return False
        




