from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import io
from PIL import Image
import base64
from Helpers import *
from logger import logger

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def upload_image():
    mydb = mysql.connector.connect(
      host="localhost",
      user="sathya",
      passwd="password",
      database="classroomdb"
    )
    mycursor = mydb.cursor()
    
    metrics.emit(UploadImageStartEvent())
    span = tracer.spanBuilder("BFS").startSpan()
    parentSpan = span;
    
    images = []
    for file in request.files.getlist("file[]"):
        logger.log("***************************")
        logger.log("image: ", file)
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            childSpan = tracer.spanBuilder("File " + file).setParent(Context.current().of(parentSpan)).startSpan();
            parentSpan = childSpan;
            
            filename = secure_filename(file.filename)
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            ratio = image.shape[0] / 500.0
            orig = image.copy()
            image = Helpers.resize(image, height = 500)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            result = "Not Blurry"

            if fm < 100:
              result = "Blurry"

            sharpness_value = "{:.0f}".format(fm)
            message = [result,sharpness_value]

            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            file_object = io.BytesIO()
            img= Image.fromarray(Helpers.resize(img,width=500))
            img.save(file_object, 'PNG')
            mycursor.execute(img)
            mydb.commit()
            base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')
            images.append([message,base64img])
            
            childSpan.end();

    metrics.emit(UploadImageEndEvent())
    logger.log("images:", len(images))
    span.end();
    return render_template('upload.html', images=images)