#ADGSTUDIOS - server.py
import base64
from io import StringIO
import os
from PIL import Image
from flask import Flask,render_template,send_from_directory,request
import hw as handwriting
from email.mime import image
import cv2
import numpy as np
app = Flask(__name__,template_folder='./hwr-app/build',static_folder='./hwr-app/build/static')



def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)                    
    return img

@app.route('/predict',methods=['POST'])
def rendertext():
    #get image from request
    if request.method == 'POST':
        if request.data:
            # read json data from request
            data = request.get_json()
            # read base64 image to cv2
            image = readb64(data['image'])
            
            # make mask of where the transparent bits are
            trans_mask = image[:, :, 3] == 0
            # replace areas of transparency with white and not transparent
            image[trans_mask] = [255, 255, 255, 255]
            # new image without alpha channel...
            new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
            result = handwriting.predict_text(new_img)
            render_result = handwriting.render_result(new_img, result)
            #return image as base64
            return {'imagedata':base64.b64encode(cv2.imencode('.jpg', render_result)[1])}
    return {'imagedata':'error'}

# allows for files to be refreshed in server
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
  return render_template('/index.html')

#running server on port 8000 - you can change the values here
if __name__ == "__main__":
  try:
    # get current working directory
    cwd = os.getcwd()
    # get the path to the hwr-app folder
    path = os.path.join(cwd, 'hwr-app')
    # change the working directory to the hwr-app folder
    os.chdir(path)
    os.system('npm run build')
  except:
    pass
    

  app.run(host="0.0.0.0",port=8000,debug=True)