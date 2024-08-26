import face_recognition
import cv2
import numpy as np
from gridfs import GridFS
import pytz
from datetime import datetime
from sklearn.neighbors import KDTree

class FaceRecognitionModule:
    def __init__(self, db):
        self.db = db
        self.fs = GridFS(db)
        self.known_face_encodings, self.known_face_names = self.load_images_from_db()
        self.face_tree = self.build_face_tree()

    def load_images_from_db(self):
        known_face_encodings = []
        known_face_names = []
        
        for face in self.db.faces.find():
            image = self.fs.get(face['image_id']).read()
            image_array = np.frombuffer(image, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            encoding = face_recognition.face_encodings(image)
            
            if len(encoding) > 0:
                known_face_encodings.append(encoding[0])
                known_face_names.append(face['name'])
        
        return known_face_encodings, known_face_names

    def build_face_tree(self):
        if self.known_face_encodings:
            return KDTree(np.array(self.known_face_encodings))
        return None

    def add_face(self, image_id, name):
        image = self.fs.get(image_id).read() 
        image_array = np.frombuffer(image, dtype=np.uint8) 
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        encoding = face_recognition.face_encodings(image)
        
        if len(encoding) > 0:
            self.known_face_encodings.append(encoding[0]) 
            self.known_face_names.append(name)
            self.db.faces.insert_one({
                'name': name,
                'image_id': image_id
            })
            self.face_tree = self.build_face_tree()  # Rebuild the tree
        else:
            print(f"No face found in {name}. Skipping...")

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            name = "Unknown"
            if self.face_tree:
                distances, indices = self.face_tree.query([face_encoding], k=1)
                if distances[0][0] < 0.6:  # Adjust this threshold as needed
                    name = self.known_face_names[indices[0][0]]
                
                    # Record recognition time if it's the first time today
                    now = datetime.now(pytz.timezone('Asia/Kolkata'))
                    date_str = now.strftime('%Y-%m-%d')
                    existing_entry = self.db.recognitions.find_one({'name': name, 'date': date_str})
                
                    if not existing_entry:
                        self.db.recognitions.insert_one({
                            'name': name,
                            'time': now.strftime('%Y-%m-%d %H:%M:%S'),
                            'date': date_str
                        })

            face_names.append(name)

        return [{'location': loc, 'name': name} for loc, name in zip(face_locations, face_names)]