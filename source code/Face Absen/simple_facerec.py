import face_recognition
import cv2
import os
import numpy as np
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import io

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_resizing = 1.5  # Increase this to improve detection from a distance

    def authenticate_google_drive(self):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service

    def load_encoding_images_from_drive(self, folder_id):
        service = self.authenticate_google_drive()
        
        results = service.files().list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/'",
            pageSize=1000, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        
        print(f"{len(items)} encoding images found.")
        
        for item in items:
            request = service.files().get_media(fileId=item['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)
            file_bytes = np.asarray(bytearray(fh.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get encoding
            img_encodings = face_recognition.face_encodings(rgb_img)
            if len(img_encodings) > 0:
                img_encoding = img_encodings[0]
                # Ensure encoding is valid before appending
                if img_encoding.shape == (128,):
                    # Remove file extension
                    file_name = os.path.splitext(item['name'])[0]
                    self.known_face_encodings.append(img_encoding)
                    self.known_face_names.append(file_name)
                else:
                    print(f"Invalid encoding for image {item['name']}")
            else:
                print(f"No face found in image {item['name']}")
        print("Encoding images loaded")

    def getlist_name(self):
        return self.known_face_names

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            else:
                name = "Unknown"
            face_names.append(name)

        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
