import os, io
import base64 
from PIL import Image
import cv2
import numpy as np
from flask import *
from rast import ndvi_caclucate_landsat7

if (__name__=='__main__'):
	app = Flask(__name__)
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.config['UPLOAD_EXTENSIONS'] = ['.tif']

@app.route('/')
def index():
	return render_template('process.html')

def get_uri(img):
	img = Image.fromarray(img.astype("uint8"))
	rawBytes = io.BytesIO()
	img.save(rawBytes, "JPEG")
	rawBytes.seek(0)
	img_base64 = base64.b64encode(rawBytes.getvalue()).decode('ascii')
	mime = "image/jpeg"
	return "data:%s;base64,%s"%(mime, img_base64)

@app.route('/', methods=['POST'])
def upload_files():
	files = request.files.getlist('file')
	if (request.files['file'].filename == ''):
		return ('', 204)
	for uploaded_file in files:
		if filename != '':
			file_ext = os.path.splitext(filename)[1]
			if file_ext not in app.config['UPLOAD_EXTENSIONS']:
				abort(400)
			npimg = np.fromstring(uploaded_file.read(),np.uint8)
			img = cv2.cvtColor(cv2.imdecode(npimg,cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
			img = Image.fromarray(img.astype("uint8"))
			if "B4.tif" in filename:
				red_image = Image.open(uploaded_file.stream)
			else:
				nir_image = Image.open(uploaded_file.stream)

	if red_image == None or nir_image == None:
		 abort(400)

	ndvi = ndvi_caclucate_landsat7(nir_image, red_image)
	greyscale = ((ndvi + 1.)/2.) * 256.
    	heatmap = cv2.cvtColor(cv2.applyColorMap(greyscale.astype('uint8'), cv2.COLORMAP_SUMMER), cv2.COLOR_BGR2RGB)
	uri = get_uri(heatmap)

	return render_template('result.html', image=uri)

if (__name__=='__main__'):
	app.run()
