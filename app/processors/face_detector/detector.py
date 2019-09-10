import face_recognition
from PIL import Image, ImageDraw
from io import BytesIO
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def face_recog(id, filename):
    unknown_image = face_recognition.load_image_file(os.path.join(BASE_DIR, 'media/%s'%(filename)))
    face_locations = face_recognition.face_locations(unknown_image)
    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)
    for face_location in face_locations:
        top, right, bottom, left = face_location
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    
    del draw

    print('finished')

    imgByteArr = BytesIO()
    pil_image.save(imgByteArr, format='PNG')

    return {
        'id': id,
        'face': imgByteArr
    }

# face_recog(1,'app/processors/face_detector/my_picture.jpg')