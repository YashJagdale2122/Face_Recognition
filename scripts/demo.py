"""
Initial face recognition experiment.
Used to validate feasibility before backend refactor.
"""

from PIL import Image, ImageDraw
import face_recognition

image_of_salman = face_recognition.load_image_file('./images/salman.jpg')
salman_encoding = face_recognition.face_encodings(image_of_salman)[0]

image_of_sharukh = face_recognition.load_image_file('./images/sharukh.jpg')
sharukh_encoding = face_recognition.face_encodings(image_of_sharukh)[0]

image_of_amir = face_recognition.load_image_file('./images/amir.jpg')
amir_encoding = face_recognition.face_encodings(image_of_amir)[0]

image_of_saif = face_recognition.load_image_file('./images/saif.jpg')
saif_encoding = face_recognition.face_encodings(image_of_saif)[0]

known_face_encoding = [
    sharukh_encoding,
    salman_encoding,
    amir_encoding,
    saif_encoding
]

known_face_names = [
    "Sharukh Khan",
    "Salman Khan",
    "Amir Khan",
    "Saif Ali Khan"
]

test_image = face_recognition.load_image_file('./images/sssa.jpg')

face_location = face_recognition.face_locations(test_image)
face_encoding = face_recognition.face_encodings(test_image, face_location)

pil_image = Image.fromarray(test_image)

draw = ImageDraw.Draw(pil_image)

for (top, right, bottom, left), encoding in zip(face_location, face_encoding):
    match = face_recognition.compare_faces(known_face_encoding, encoding)
    name = "Unknown"
    if True in match:
        First = match.index(True)
        name = known_face_names[First]
    draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0))

    draw.text((left, bottom), name, fill='white', stroke_width=1, stroke_fill='black', font_size=bottom/24)
del draw
pil_image.show()
