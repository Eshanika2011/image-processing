import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    operation_selection = request.form['image_type_selection']
    image_file = request.files['file']
    filename = secure_filename(image_file.filename)
    reading_file_data = image_file.read()
    image_array = np.fromstring(reading_file_data, dtype='uint8')
    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)


    # Write code for Select option for Gray and Sketch
    if operation_selection=='gray':
        file_data=make_grayscale(decode_array_to_img)
    elif operation_selection=='sketch':
        file_data=image_sketch(decode_array_to_img)
    elif operation_selection=='oil':
        file_data=oil_effect(decode_array_to_img)
    elif operation_selection=='rgb':
        file_data=rgb_effect(decode_array_to_img)














    # Ends here

    with open(os.path.join('static/', filename),
                  'wb') as f:
        f.write(file_data)

    return render_template('upload.html', filename=filename)

def make_grayscale(decode_array_to_img):

    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)

    return output_image


# Write code for Sketch function
def image_sketch(decode_array_img):
    c_gray_image=cv2.cvtColor(decode_array_img,cv2.COLOR_BGR2GRAY)
    sharp_img=cv2.bitwise_not(c_gray_image)
    blur_img=cv2.GaussianBlur(sharp_img,(111,111),0)
    sharp_blur_img=cv2.bitwise_not(blur_img)
    sketch_img=cv2.divide(c_gray_image,sharp_blur_img,scale=256.0)
    status, output_image = cv2.imencode('.PNG',sketch_img)
    return output_image

def oil_effect(decode_array_img):
    oil_effect_img=cv2.xphoto.oilPainting(decode_array_img,6,1)
    status, output_image = cv2.imencode('.PNG',oil_effect_img)
    return output_image

def rgb_effect(decode_array_img):
    rgb_effect_img=cv2.cvtColor(decode_array_img,cv2.COLOR_BGR2RGB)
    status, output_image = cv2.imencode('.PNG',rgb_effect_img)
    return output_image





# Ends here


@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()










