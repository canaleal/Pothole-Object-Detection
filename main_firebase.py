import logging

import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

logging.basicConfig(level=logging.INFO)

import uuid

def save_to_firebase(user_id, local_output_path):
    try:
        logging.info('Uploading to Firebase')
        cred = credentials.Certificate('main_capstone.json')
        firebase_admin.initialize_app(cred,
                                      {
                                          'databaseURL': 'https://Capstone.firebaseio.com/'
                                      })
        db = firestore.client()
        
        # Create the collections paths
        collection_name = str(uuid.uuid4()) + '-potholes'
        doc_ref = db.collection('users').document(user_id).collection(collection_name)

        # Import data
        local_output_path_file = local_output_path + '/output.csv'
        df = pd.read_csv(local_output_path_file)
        tmp = df.to_dict(orient='records')
        list(map(lambda x: doc_ref.add(x), tmp))
        logging.info('Finished uploading to Firebase')

    except Exception as e:
        logging.error('Unable to save results to Firebase')


if __name__ == '__main__':
    print(0)
