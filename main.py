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


def algorithm(user_id, raw_link_vid, raw_link_coord):

    if user_id is None:
        logging.error('User ID is None')
        sys.exit()

    if raw_link_vid == "" and raw_link_coord == "":
        logging.error("No links provided.")
        sys.exit()


    #----------------------------------------------------------------------------------------------------------------------
 
    # Local Save path
    input_path = 'model_input'
    video_path = 'model_input/video'
    coord_path = 'model_input/coord'
    frame_path = 'model_input/frame'
    output_path = 'model_output'
    runs_path = 'runs/detect'

    try:
        # check if folder exists and create if not
        main_util.checkIfFolderExistsAndCreateIfNot(input_path)
        main_util.checkIfFolderExistsAndCreateIfNot(video_path)
        main_util.checkIfFolderExistsAndCreateIfNot(coord_path)
        main_util.checkIfFolderExistsAndCreateIfNot(frame_path)
        main_util.checkIfFolderExistsAndCreateIfNot(output_path)
        main_util.checkIfFolderExistsAndCreateIfNot(runs_path)
    except Exception as e:
        logging.error(e)
        sys.exit()

    #----------------------------------------------------------------------------------------------------------------------
    try:
        # Load Google Drive Files and save them locally
        main_gdownloader.download_google_file(raw_link_vid, video_path + '/video.mp4')
        main_gdownloader.download_google_file(raw_link_coord, coord_path + '/coord.csv')
        main_video.convert_video_to_frames(video_path + '/video.mp4', frame_path)
    except Exception as e:
        logging.error(e)
        sys.exit()

    try:
        callSubProcess('python detect.py --weights best.pt --source model_input/frame')
    except Exception as e:
        logging.error(e)
        sys.exit()
    
    #----------------------------------------------------------------------------------------------------------------------
    try:
        # Save to firebase
        database = main_firebase.load_firebase('main_capstone.json')

        if database is None:
            raise Exception('Unable to load Firebase database')

        collection_reference = main_firebase.get_firebase_collection(database, user_id)

        if collection_reference is None:
            raise Exception('Unable to load Firebase collection')

        data = main_firebase.load_data_from_csv(output_path + '/output.csv')
        geojson = main_firebase.convert_data_to_geojson(data)
        main_firebase.save_data_to_firebase(collection_reference, geojson)
        
    except Exception as e:
        logging.error(e)
        sys.exit()
   
   
    #----------------------------------------------------------------------------------------------------------------------
    try:
        # Delete input files and Delete output files
        main_util.deleteAllFilesInFolder(video_path)
        main_util.deleteAllFilesInFolder(coord_path)
        main_util.deleteAllFilesInFolder(frame_path)
        main_util.deleteAllFilesInFolder(output_path)
        main_util.deleteAllFoldersInFolder(runs_path)
    except Exception as e:
        logging.error(e)
        sys.exit()
        
        

if __name__ == "__main__":
    user_id = '0tk8sTPDuwR2WM7lFyUn4OxjGLr1'
    video_link = 'https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing'
    coord_link = 'https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing'
    algorithm(user_id, video_link, coord_link)
    
    

# if __name__ == "__main__":

#     st.markdown('Showcase Application - Web')
#     st.markdown('**This application is used to demonstrate the use of the YOLOv5 algorithm.**')
#     st.markdown('User Id: 0tk8sTPDuwR2WM7lFyUn4OxjGLr1')
#     st.markdown('Video : https://drive.google.com/file/d/1C2p3HuuBuzhuG8hkeMnEcKxhTOL5qbqg/view?usp=sharing')
#     st.markdown('Coordinates : https://drive.google.com/file/d/1qs5Wcj4haLuEoqDUMdEF4VidrdyaOyY7/view?usp=sharing')

#     # Create variables used to contain the link to the video and the coordinates
#     user_id = ''
#     video_link = ''
#     coord_link = ''

#     # Create a text input widget to get the link to the video and the coordinates
#     with st.form(key='my_form', clear_on_submit=True):
#         user_id = st.text_input('User ID', user_id)
#         video_link = st.text_input('Video Link - Required', video_link)
#         coord_link = st.text_input('Coordinates Link - Required', coord_link)

#         submit_button = st.form_submit_button('Run Algorithm')

#     # If the submit button is clicked, run the algorithm
#     if submit_button:

#         if (user_id != '') and (video_link != '') and (coord_link != ''):
#             st.success('Starting the algorithm...')
#             algorithm(user_id, video_link, coord_link)
#             st.success('Done')

#         else:
#             st.error('Video and Coordinates are required.')
