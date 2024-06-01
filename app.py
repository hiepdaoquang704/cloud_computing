from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model = load_model('/home/hiepdaoquang704/cloud_computing/dog_and_model.h5')

# Define classes
classes = ['Cat', 'Dog']

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            image = load_img(filepath, target_size=(64, 64))  
            image = img_to_array(image)  
            image = image / 255.0 
            image = np.expand_dims(image, axis=0)  
            
            prediction = model.predict(image)
            print(prediction)
            if prediction[0][0]==1:
                predication='dog'
            else:
                predication='cat'
            return render_template('index.html', filename=filename, prediction=predication)
    
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)


    