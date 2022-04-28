import logging
import uuid
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

logging.basicConfig(level=logging.INFO)


def load_firebase(credentials_file):
    try:
        cred = credentials.Certificate(credentials_file)
        firebase_admin.initialize_app(cred,
                                      {
                                          'databaseURL': 'https://Capstone.firebaseio.com/'
                                      })
        return firestore.client()

    except ValueError as e:
        logging.error(e)
        return None


def set_firebase_collection(db, user_id):
    try:
        collection_name = str(uuid.uuid4()) + '-potholes'
        document_reference = db.collection('users').document(user_id).collection(collection_name)
        return document_reference

    except ValueError as e:
        logging.error(e)
        return None


def load_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    tmp = df.to_dict(orient='records')
    return tmp


def save_data_to_firebase(document_reference, data):
    try:
        list(map(lambda x: document_reference.add(x), data))
        return True
    except ValueError as e:
        logging.error(e)
        return False


def save_to_firebase(user_id, local_output_path):
    try:
        logging.info('Uploading to Firebase')
        db = load_firebase('main_capstone.json')

        if db is None:
            logging.error('Unable to load Firebase')
            return False

        document_reference = set_firebase_collection(db, user_id)

        if document_reference is None:
            logging.error('Unable to upload to Firebase')
            return False

        data = load_data_from_csv(local_output_path + '/output.csv')
        result = save_data_to_firebase(document_reference, data)

        logging.info('Finished uploading to Firebase')

    except ValueError:
        logging.error(ValueError)


if __name__ == '__main__':
    print(0)
