
import requests
from flask import Flask, request, render_template
import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_googlemaps import GoogleMaps
from PIL import Image

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAYDG5-pVx-x21tWZy2ysZRL6rAKS5mFts"

GoogleMaps(app)
CWD = os.getcwd()
UPLOAD_FOLDER = CWD
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# user sends coordinates and the api loads form
@app.route('/getImage', methods=['GET'])
def getImage():
    parameters = request.args
    latitude = None
    longitude = None
    if "latitude" in parameters and "longitude" in parameters:
        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")
    else:
        return "Please provide latitude and longitude"
    return render_template('form.html', coordinates = {'lat' : latitude, 'long' : longitude})

# saves the client image and process it
@app.route('/uploadProcess', methods = ['POST'])
def uploadProcess():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    parameters = request.args
    latitude = None
    longitude = None
    if "latitude" in parameters:
        latitude = request.args.get("latitude")
    if "longitude" in parameters:
        longitude = request.args.get("longitude")

    get_map(latitude,longitude)
    overlay_image()
    return f"Your image has been overlayed on map at latitude = {latitude} and longitude = {longitude}"

#downloads the processed image
@app.route('/download', methods=['GET'])
def download():
    global new_img
    new_img.save('new.png', "PNG")
    return "saved"
def get_map(latitude, longitude):
    key = "AIzaSyAYDG5-pVx-x21tWZy2ysZRL6rAKS5mFts"
    r = requests.get(f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=10&size=400x400&key={key}&maptype=satellite")
    f = open('final.png', 'wb')
    f.write(r.content)
    f.close()

# adds an overlay to the map figure
def overlay_image():
    background2 = Image.open("final.png")
    overlay = Image.open("plume.png")
    background2 = background2.resize((514,257))  # resizes the image from google maps
    print("2 SIZE ", background2.size)

    background2 = background2.convert("RGBA")
    overlay = overlay.convert("RGBA")

    global new_img
    new_img = Image.blend(background2, overlay, 0.25)
   
if __name__ == '__main__':
    global new_img
    new_img = None
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

