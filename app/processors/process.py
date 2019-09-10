from concurrent.futures import ThreadPoolExecutor
from app.processors.classifier.recog import classify
from app.processors.face_recognition.test import face_recog
from app.models import Record
import json

pool = ThreadPoolExecutor(4)

def update(res):
    data = res.result()
    try:
        record = Record.objects.get(pk=data['id'])
        record.classify=json.dumps(data['res'])
        record.save()
    except:
        print('error')

def process_classify(id, filename):
    pool.submit(classify, id, filename).add_done_callback(update)

def process_facerecog(id, filename):
    pool.submit(face_recog, id, filename).add_done_callback(update)
