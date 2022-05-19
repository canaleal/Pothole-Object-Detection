from datetime import datetime
import logging
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore


def load_firebase(credentials_file):
    credentials = credentials.Certificate(credentials_file)
    firebase_admin.initialize_app(credentials,
                                  {
                                      'databaseURL': 'https://Capstone.firebaseio.com/'
                                  })
    return firestore.client()


def get_firebase_collection(db, user_id):
    return db.collection('users').document(user_id).collection('potholes')


def load_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    data = df.to_dict(orient='records')
    return data


def convert_data_to_geojson(data):
    geojson = {"type": "FeatureCollection", "date_time_analyzed": datetime.now(), "features": []}
    for point in data:
        temp_point = point
        coordinate = [float(temp_point['long']), float(temp_point['lat'])]
        temp_point.pop('long')
        temp_point.pop('lat')

        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coordinate},
            "properties": temp_point}

        geojson['features'].append(feature)

    return geojson


def save_data_to_firebase(document_reference, geojson):
    document_reference.add(geojson)


if __name__ == '__main__':
    print(0)
