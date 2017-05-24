# http://stackoverflow.com/questions/43309343/working-with-user-uploaded-image-in-flask?noredirect=1&lq=1

# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import main_uploaded
import os
from werkzeug import secure_filename

''' look at later
http://htmlcolorcodes.com/resources/ultimate-guide-to-free-stock-photos/
'''
# to run:
'''
to run, use commands below:
    python src/webapp.py
'''

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
dirpath = '/Users/colinbottles/Desktop/Cat/school/color-match/uploads'
app.config['UPLOAD_FOLDER'] = dirpath
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['jpg'])


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# This route will show the initial user submit form to perform an AJAX request
# jQuery is loaded to execute the request and update the value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the results route, which
        # will show on the browser the model output
        return redirect(url_for('results'))


# This route will show the results form that displays the model output
# in a user friendly format
@app.route('/results', methods=['GET'])
def results():
    path = '/Users/colinbottles/Desktop/Cat/school/color-match/uploads/'
    clust_pred, suggbf, sugg1, sugg2, suggb = main_uploaded.analyzer(path)
    return render_template('results.html',
                           clust_pred=clust_pred, suggbf=suggbf,
                           sugg1=sugg1, sugg2=sugg2,
                           suggb=suggb)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = 5000
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
