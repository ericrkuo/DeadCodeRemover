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

@app.route('/', methods=['POST'])
def upload_image():
    logger.log("Initializating trace provider")

    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    logger.log("Initializating DB connection")
    mydb = mysql.connector.connect(host="localhost",
                                   user="sathya",
                                   passwd="password",
                                   database="classroomdb")
    mycursor = mydb.cursor()
    logger.log("Established DB connection")

    metrics.emit(UploadImageStartEvent())
    span = tracer.spanBuilder("POST - Upload Image").startSpan()
    parentSpan = span

    if not (request.files and request.files.getlist("file[]") and len(request.files.getlist("file[]"))):
      logger.log(f"Error: no files could be found of request {request}")
      return "No files found", 400

    images = []
    for file in request.files.getlist("file[]"):
        logger.log("***************************")
        logger.log("image: ", file)

        if file.filename == '':
            logger.log('No image selected for uploading')
            flash('No image selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            childSpan = tracer.start_as_current_span("File " + FileHelper.getName(file))
            childSpan.setParent(Context.current().of(parentSpan)).startSpan()
            childSpan.setAttribute("Size", FileHelper.getSize(file))
            childSpan.setAttribute("Extension", FileHelper.getExtension(file))
            childSpan.setAttribute("Author", FileHelper.getAuthor(file))
            parentSpan = childSpan

            filename = secure_filename(file.filename)
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            logger.log("Commiting raw image to DB")
            mycursor.execute(image)
            mydb.commit()
            logger.log("Commited raw image to DB")

            # format image
            image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            ratio = image.shape[0] / 500.0
            image = Helpers.resize(image, height=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            result = "Not Blurry"

            if fm < 100:
                metrics.emit(BlurryImageevent(fm))
                result = "Blurry"

            sharpness_value = "{:.0f}".format(fm)
            message = [result, sharpness_value]

            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            file_object = io.BytesIO()
            img = Image.fromarray(Helpers.resize(img, width=500))
            img.save(file_object, 'PNG')
            logger.log("Commiting formatted image to DB")
            mycursor.execute(img)
            mydb.commit()
            logger.log("Commited formatted image to DB")
            base64img = "data:image/png;base64," + base64.b64encode(file_object.getvalue()).decode('ascii')
            images.append([message, base64img])

            logger.log(f"Finished formatting and uploading image in file {file.filename}")
            childSpan.end()

        metrics.emit(UploadImageEndEvent())
        logger.log("images:", len(images))
        span.end()
        return render_template('upload.html', images=images)
