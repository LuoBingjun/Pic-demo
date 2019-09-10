from concurrent.futures import ThreadPoolExecutor
from django.core.files.uploadedfile import InMemoryUploadedFile

from app.processors.classifier.recog import classify
from app.processors.face_detector.detector import face_recog
from app.models import Record
import json

pool = ThreadPoolExecutor(4)

def update_classify(res):
    data = res.result()
    try:
        record = Record.objects.get(pk=data['id'])
        record.classify=json.dumps(data['res'])
        record.save()
    except:
        print('error')

def update_face(res):
    data = res.result()
    face = data['face']
    file = InMemoryUploadedFile(face, None, 'face.png', None, len(face.getvalue()), None, None)
    try:
        record = Record.objects.get(pk=data['id'])
        record.face = file
        record.save()
    except:
        print('error')

def process_classify(id, filename):
    pool.submit(classify, id, filename).add_done_callback(update_classify)

def process_facerecog(id, filename):
    pool.submit(face_recog, id, filename).add_done_callback(update_face)
