from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin

from classes.CountingClass import Chickount
from secret import firestore_admin

cred = credentials.Certificate(firestore_admin)
app = firebase_admin.initialize_app()

def UploadDataToFirestore(data,idRef, collection_name = 'yolo'):
    db = firestore.client()
    q = db.collection('esp').document(idRef).get().to_dict()

    up = Chickount(uname=q['uname'], 
                     part=q['cam_part'], 
                     idRef=idRef, 
                     image=data['image'], 
                     count=data['count'],
                     timestamp=q['timestamp'])
    doc_ref = db.collection(collection_name).add(up.to_dict())

    return doc_ref[1].id

def GetImageFromFirestore(idRef = None, collection_name = 'esp'):
    db = firestore.client()
    
    q = db.collection(collection_name).document(idRef).get().to_dict()
    img = q['image']

    img_base64 = img.split(',')[1]

    return img_base64