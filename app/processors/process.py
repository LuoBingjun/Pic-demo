from concurrent.futures import ThreadPoolExecutor
from app.processors.classifier.recog import classify
from app.models import Record

pool = ThreadPoolExecutor(4)

def update(res):
    data = res.result()
    try:
        record = Record.objects.get(pk=data['id'])
        record.classify=str(data['res'])
        record.save()
    except:
        print('error')

def process_classify(id, filename):
    pool.submit(classify, id, filename).add_done_callback(update)