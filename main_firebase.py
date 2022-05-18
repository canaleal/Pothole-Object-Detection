from datetime import datetime
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
        collection_name = 'potholes'
        document_reference = db.collection('users').document(user_id).collection(collection_name)
        return document_reference

    except ValueError as e:
        logging.error(e)
        return None


def load_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    tmp = df.to_dict(orient='records')
    return tmp


def convert_data_to_geojson(data):
    geojson = { "type": "FeatureCollection", "date_time_analyzed": datetime.now().strftime('%Y-%m-%d %H:%M:%S') ,"features": [] }
    for point in data :
        temp_point = point
        coordinate = [float(temp_point['long']), float(temp_point['lat'])]
        temp_point.pop('long')
        temp_point.pop('lat')
        feature = { "type": "Feature", "geometry": { "type": "Point", "coordinates": coordinate }, "properties": temp_point }
        geojson['features'].append(feature)
        
    return geojson
    

def save_data_to_firebase(document_reference, data):
    try:
        geojson = convert_data_to_geojson(data)
        document_reference.add(geojson)
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
