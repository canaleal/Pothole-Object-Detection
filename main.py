
import sys

import logging
import main_util
import main_gdownloader
import subprocess


def waitTillProgramIsDone(command):   
    subprocess.call(command, shell=True)
    while True:
        if subprocess.call(command, shell=True) == 0:
            break
        else:
            continue


def algorithm(raw_link_vid , raw_link_coord ):
    
    if raw_link_vid == "" and raw_link_coord == "":
        logging.error("No links provided.")
        sys.exit()

    # Local Save path
    temp_local_save_path = 'model_input'

    # check if folder exists and create if not
    main_util.checkIfFolderExistsAndCreateIfNot(temp_local_save_path)

    # Load Google Drive Files and save them locally
    main_gdownloader.downloadGoogleDriveFiles(raw_link_vid, raw_link_coord, temp_local_save_path)

    # waitTillProgramIsDone('python3 detect.py --weights best.pt --source input')
    
    # Delete input files
    main_util.deleteFileIfItExists(temp_local_save_path + "/video.mp4")
    main_util.deleteFileIfItExists(temp_local_save_path + "/coord.csv")


if __name__ == "__main__":
    video_link = 'https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing'
    coord_link = 'https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing'
    algorithm(video_link, coord_link)



import streamlit as st

if __name__ == "__main__":

    st.markdown('Showcase Application - Web')
    st.markdown('**This application is used to demonstrate the use of the YOLOv5 algorithm.**')
    st.markdown('Video : https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing')
    st.markdown('Coordinates : https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing')

    # Create variables used to contain the link to the video and the coordinates
    video_link = ''
    coord_link = ''

    # Create a text input widget to get the link to the video and the coordinates
    with st.form(key='my_form', clear_on_submit=True):
        video_link = st.text_input('Video Link - Required', video_link)
        coord_link = st.text_input('Coordinates Link - Required', coord_link)

        submit_button = st.form_submit_button('Run Algorithm')

    # If the submit button is clicked, run the algorithm
    if submit_button:

        if (video_link != '') and (coord_link != ''):
            st.success('Starting the algorithm...')
            algorithm(video_link, coord_link)
            st.success('Done')
            
        else:
            st.error('Video and Coordinates are required.')