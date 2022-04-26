
import gdown
import re
import sys
import os
import logging


def download_google_file(url, filename):
    try:
        logging.info("Downloading starts...")
        gdown.download(url, filename, quiet=False)
    except ValueError:
        logging.error(ValueError)
        
        
def strip_link_from_raw_url(raw_link):
    result = re.search('https://drive.google.com/file/d/(.*)', raw_link)
    file_id = re.sub('/view\?usp=sharing', '', result.group(1))
    url = f'https://drive.google.com/uc?id={file_id}'
    return url


def downloadGoogleDriveFiles(video_link, csv_link, save_path):


    try:
        
        url_video = strip_link_from_raw_url(video_link)
        output_video = f'{save_path}/video.mp4'

        url_coord = strip_link_from_raw_url(csv_link)
        output_coord = f'{save_path}/coord.csv'
        
        download_google_file(url_video, output_video)
        download_google_file(url_coord, output_coord)
    except ValueError:
        logging.error('Unable to download video and csv.')
        sys.exit()
        
