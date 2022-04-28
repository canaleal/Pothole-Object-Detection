import sys

import logging
import main_util
import main_gdownloader
import main_firebase
import main_video
import subprocess
import streamlit as st


def callSubProcess(command):
    subprocess.call(command, shell=True)


def waitTillProgramIsDone(command):
    subprocess.call(command, shell=True)
    while True:
        if subprocess.call(command, shell=True) == 0:
            break
        else:
            continue


def algorithm(user_id, raw_link_vid, raw_link_coord):
    if raw_link_vid == "" and raw_link_coord == "":
        logging.error("No links provided.")
        sys.exit()

    # Local Save path
    input_path = 'model_input'
    video_path = 'model_input/video'
    coord_path = 'model_input/coord'
    frame_path = 'model_input/frame'

    output_path = 'model_output'
    runs_path = 'runs/detect'

    # check if folder exists and create if not
    main_util.checkIfFolderExistsAndCreateIfNot(input_path)
    main_util.checkIfFolderExistsAndCreateIfNot(video_path)
    main_util.checkIfFolderExistsAndCreateIfNot(coord_path)
    main_util.checkIfFolderExistsAndCreateIfNot(frame_path)

    main_util.checkIfFolderExistsAndCreateIfNot(output_path)
    main_util.checkIfFolderExistsAndCreateIfNot(runs_path)

    # Load Google Drive Files and save them locally
    main_gdownloader.download_google_file(raw_link_vid, video_path + '/video.mp4')
    main_gdownloader.download_google_file(raw_link_coord, coord_path + '/coord.csv')

    main_video.convert_video_to_frames(video_path + '/video.mp4', frame_path)

    callSubProcess('python detect.py --weights best.pt --source model_input/frame')

    # Save to firebase
    main_firebase.save_to_firebase(user_id, output_path)

    # Delete input files
    main_util.deleteAllFilesInFolder(video_path)
    main_util.deleteAllFilesInFolder(coord_path)
    main_util.deleteAllFilesInFolder(frame_path)

    # Delete output files
    main_util.deleteAllFilesInFolder(output_path)
    main_util.deleteAllFoldersInFolder(runs_path)


if __name__ == "__main__":
    user_id = '0tk8sTPDuwR2WM7lFyUn4OxjGLr1'
    video_link = 'https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing'
    coord_link = 'https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing'
    algorithm(user_id, video_link, coord_link)

if __name__ == "__main__":

    st.markdown('Showcase Application - Web')
    st.markdown('**This application is used to demonstrate the use of the YOLOv5 algorithm.**')
    st.markdown('User Id: 0tk8sTPDuwR2WM7lFyUn4OxjGLr1')
    st.markdown('Video : https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing')
    st.markdown('Coordinates : https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing')

    # Create variables used to contain the link to the video and the coordinates
    user_id = ''
    video_link = ''
    coord_link = ''

    # Create a text input widget to get the link to the video and the coordinates
    with st.form(key='my_form', clear_on_submit=True):
        user_id = st.text_input('User ID', user_id)
        video_link = st.text_input('Video Link - Required', video_link)
        coord_link = st.text_input('Coordinates Link - Required', coord_link)

        submit_button = st.form_submit_button('Run Algorithm')

    # If the submit button is clicked, run the algorithm
    if submit_button:

        if (user_id != '') and (video_link != '') and (coord_link != ''):
            st.success('Starting the algorithm...')
            algorithm(user_id, video_link, coord_link)
            st.success('Done')

        else:
            st.error('Video and Coordinates are required.')
