import face_recognition
import db_helper as db


def checkImage(img1,img2):
    known_image = face_recognition.load_image_file(img1)
    unknown_image = face_recognition.load_image_file(img2)
    biden_encoding = face_recognition.face_encodings(known_image,num_jitters=1)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image,num_jitters=1)[0]
    db.insert(biden_encoding.tolist())
    results = face_recognition.compare_faces([biden_encoding], unknown_encoding,tolerance=0.52)
    return results