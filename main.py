from fastapi import FastAPI, UploadFile, Request, Form, Query
import face_recognition
import base64
from tinydb import TinyDB, where
import numpy as np
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

db = TinyDB('database.json')

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse('home.html', {"request": request, "elements": db.all()})

@app.post("/register/")
def register(name: str = Form(), email: str = Form(), file: UploadFile = Form()):
    image = face_recognition.load_image_file(file.file)
    image_encoding = face_recognition.face_encodings(image)[0]
    encoded = base64.b64encode(image_encoding.tobytes()).decode('utf-8')
    id = db.insert({"name": name, "email": email, "encoded": encoded})
    return {
        "id": id
    }

@app.post("/recognise/")
def recognise(file: UploadFile = Form()):
    image = face_recognition.load_image_file(file.file)
    image_encoding = face_recognition.face_encodings(image)[0]
    all_encodings = []

    for i in db.all():
        all_encodings.append(np.frombuffer(base64.b64decode(i["encoded"]), dtype=np.float64))
    
    results = face_recognition.compare_faces(all_encodings, image_encoding)
    index = results.index(True)
    return {'name': db.all()[index]['name'], 'email': db.all()[index]['email']}

@app.post("/delete/")
async def delete(email: str = Form()):
    return {'removed': db.remove(where('email') == email)}

@app.post("/modify/")
async def delete(name: str = Form(), email: str = Form(), oldemail: str = Form()):
    Person = Query()
    record = db.search(where('email') == oldemail)[0]
    record['name'] = name
    record['email'] = email
    db.update(record, where('email') == oldemail)
    return {'code': 'success'}