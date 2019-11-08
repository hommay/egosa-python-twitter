import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def firestore_authorization():
    cred = credentials.Certificate(os.environ.get('FIREBASE_CREDENTIAL'))
    firebase_admin.initialize_app(cred)
    return firestore.client()