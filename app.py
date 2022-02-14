#Import the required libraries.
import os
from flask import Flask, render_template, request
from landmarks_filter import get_image_with_landmarks
#Create upload folder using flask 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
#Create a base index that transforms with results. 
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", result={})
    else:
        image = request.files["image"]
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path)
        result_from_landmarks = get_image_with_landmarks(path)
        os.remove(path)

        return render_template("index.html", result=result_from_landmarks)
#Use flask to open a web port. 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)