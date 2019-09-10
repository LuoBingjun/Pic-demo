import face_recognition
from PIL import Image, ImageDraw


def face_recog(id, filename):
    unknown_image = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(unknown_image)
    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)
    for face_location in face_locations:
        top, right, bottom, left = face_location

    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    del draw
    pil_image.show()

    return {
        'id': id,
        'pil_image': pil_image
    }

face_recog(1,'my_picture.jpg')