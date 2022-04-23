import gdown
import re
import sys
import os
import logging


def checkIfFolderExistsAndCreateIfNot(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


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
    except ValueError:
        logging.error('No link provided.')
        sys.exit()

    try:
        download_google_file(url_video, output_video)
        download_google_file(url_coord, output_coord)
    except ValueError:
        logging.error('Unable to download video and csv.')
        sys.exit()


def deleteInputFiles(local_input_path):
    try:
        video_path = f"{local_input_path}/video.mp4"
        coord_path = f"{local_input_path}/coord.csv"

        if os.path.exists(video_path):
            os.remove(video_path)
            logging.info("Video File deleted")
        else:
            logging.error("The Video File does not exist")

        if os.path.exists(coord_path):
            os.remove(coord_path)
            logging.info("Coord File deleted")
        else:
            logging.error("The CSV File does not exist")
    except ValueError:
        logging.error(ValueError)


def callProgramWithTerminalCommands(command):
    import subprocess
    subprocess.call(command, shell=True)


def waitTillProgramIsDone(command):
    import subprocess
    subprocess.call(command, shell=True)
    while True:
        if subprocess.call(command, shell=True) == 0:
            break
        else:
            continue



def algorithm(raw_link_vid = 'https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing', raw_link_coord = 'https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing'):

    local_input_path = 'model_input'

    # check if folder exists and create if not
    checkIfFolderExistsAndCreateIfNot(local_input_path)

    # Load Google Drive Files
    downloadGoogleDriveFiles(raw_link_vid, raw_link_coord, local_input_path)

    # waitTillProgramIsDone('python3 detect.py --weights best.pt --source input')
    
    # Delete input files
    deleteInputFiles(local_input_path)
    
    print('Done')

import streamlit as st

if __name__ == "__main__":
    st.markdown('Showcase Application - Web')

    st.markdown('**This application is used to demonstrate the use of the YOLOv5 algorithm.**')
    
    st.markdown('Video : https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing')
    st.markdown('Coordinates : https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing')
    
    video_link = ''
    coord_link = ''

    with st.form(key='my_form', clear_on_submit=True):

        video_link = st.text_input('Video Link - Required', video_link)
        coord_link = st.text_input('Coordinates Link - Required', coord_link)

        submit_button = st.form_submit_button('Run Algorithm')

    if submit_button:
        if (video_link != '') and (coord_link != ''):

            st.success('Starting the algorithm...')
            algorithm(video_link, coord_link)
            
            st.success('Done')
            
            
        else:
            st.error('Video and Coordinates are required.')