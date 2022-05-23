

from unicodedata import name
from flask import Flask, render_template, Response,url_for, request,redirect

import cv2
import face_recognition
import numpy as np


import sqlalchemy
from sqlalchemy import VARCHAR, insert
from urllib.parse import quote


from sqlalchemy import Table, Column, Integer, String, MetaData
from adodbapi import Timestamp


from werkzeug.utils import secure_filename
import os
from datetime import datetime
SESSION_TYPE = 'redis'
app=Flask(__name__)
app.config.from_object(__name__)
#Session(app)




meta = MetaData()

database_username = 'root'
database_password = ''
database_ip       = '127.0.0.1'
database_name     = 'face_attendance'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, quote(database_password),
                                                      database_ip, database_name))
std  = Table(
   'students', meta, 
   Column('user_id', Integer, primary_key = True), 
   Column('user_name', VARCHAR), 
   Column('image_url', VARCHAR)
)
name_="unknown"

#UPLOAD_FOLDER = '/UPLOAD_FOLDER/'
app.config["UPLOAD_FOLDER"] = "Training_images"
#base_path = os.path.abspath(os.path.dirname(__file__))
#upload_path = os.path.join(base_path, app.config['/UPLOAD_FOLDER/'])
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png','JPG','JPEG','PNG'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('a.csv', 'r+') as f:
        myDataList = f.readlines()


        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

# encodeListKnown = findEncodings(images)
# print('Encoding Complete')


camera = cv2.VideoCapture(0)
# Load a sample picture and learn how to recognize it.
krish_image = face_recognition.load_image_file("Krish/krish.jpg")
krish_face_encoding = face_recognition.face_encodings(krish_image)[0]

# Load a second sample picture and learn how to recognize it.
bradley_image = face_recognition.load_image_file("Bradley/bradley.jpg")
bradley_face_encoding = face_recognition.face_encodings(bradley_image)[0]

# Load a second sample picture and learn how to recognize it.
shuvo_image = face_recognition.load_image_file("shuvo/shuvo.jpg")
shuvo_face_encoding = face_recognition.face_encodings(shuvo_image)[0]

#known face name
known_face_names = []
#known_face_encodings = []



# Create arrays of known face encodings and their names

#known_face_names = [
 #   "Krish",
    #"Bradly",
   # "Shuvo"
#]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True



def gen_frames():  
    path = 'Training_images'
    images = []
    classNames = []
    
    myList = os.listdir(path)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
        known_face_names.append(os.path.splitext(cl)[0])
#print(classNames)

    known_face_encodings = findEncodings(images)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(imgS)
            face_encodings = face_recognition.face_encodings(imgS, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    name_=name
                    
                face_names.append(name)
            

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

@app.route('/')
def index():
    return render_template('index.html',utc_dt=name_)
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/info/')
def addInfo():
    return render_template('settings.html')
@app.route('/settings',methods = ['POST', 'GET'])
def settings():
   if request.method == 'POST':
      user = request.form['txtName']
      #userImage = request.form['txtImage']
      
      file = request.files['txtImage']
      ins = std.insert().values(user_name = user,image_url=file.filename)
      conn = database_connection.connect()
      result = conn.execute(ins)
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
      #print(userImage)
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('txtName')
      return redirect(url_for('success',name = user))
@app.route('/success/<name>')
def success(name):
   return 'Saved Successfully'
if __name__=='__main__':
    app.run(debug=True)