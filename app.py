import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import glob
from uuid import uuid4

UPLOAD_FOLDER = './test'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mkv', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def serve():

	vfiles = []
	for file in glob.glob("{}/*.mp4".format("test")):
		fname = file.split(os.sep)[-1]
		vfiles.append(fname)

	tfiles = []
	for file in glob.glob("{}/*.txt".format("test")):
		fcontent = open(file, 'r').read()
		tfiles.append(fcontent)

	return render_template('index.html',
		files=vfiles, text=tfiles)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		
		if 'file' not in request.files:
			print('no file')
			return redirect(request.url)
		file = request.files['file']
		

		if file.filename == '':
			print('no filename')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			info = request.form['info']
			with open(UPLOAD_FOLDER + '/' + filename[:-4] + '.txt', 'w') as f:
				f.write(info)

			os.system("cd test; ls")
			
			return render_template('index.html')
			#return redirect(url_for('uploaded_file', filename=filename))


	return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)


if __name__ == "__main__":
	app.run(debug=True)