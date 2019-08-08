import os
#import magic
import urllib.request
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from flask import Flask, send_file
import zipfile
import io
import shutil
import pathlib


UPLOAD_FOLDER='/tmp/uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        os.makedirs('/tmp/uploads', exist_ok=True)
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       # Code to zip all the uploaded files
        base_path = pathlib.Path('/tmp/uploads/')
        data = io.BytesIO()
        with zipfile.ZipFile(data, mode='w') as z:
            for f_name in base_path.iterdir():
                z.write(f_name)
        data.seek(0)
        shutil.rmtree('/tmp/uploads')
        flash('File(s) successfully uploaded')
        return send_file(data,
            mimetype='application/zip',
            as_attachment=True,
            attachment_filename='data.zip'
            )
        # return redirect('/')

if __name__ == "__main__":
    app.run()
