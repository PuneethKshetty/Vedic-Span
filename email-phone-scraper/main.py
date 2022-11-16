from importlib.resources import path
from flask import Flask, render_template, request, send_from_directory, current_app
from scrape import getEmailAndPhone
from genCSV import generateCSV
import os

app = Flask(__name__)

# storedData = {
# 	'phoneList': [],
# 	'emailList': [],
# }

@app.route("/", methods=["POST", "GET"])
def home(data=None, status=-1, maxlen=0):
	if request.method == "POST":
		url = request.form['url-input']
		urlList = url.split(",")

		# print(url)
		try:
			data = getEmailAndPhone(urlList)
			status = 0

			if (len(data['phoneList']) > len(data['emailList'])):
				maxlen = len(data['phoneList'])
			else:
				maxlen = len(data['emailList'])

			generateCSV(data)

			if maxlen == 0:
				status = 2
		
		except:
			status = 1

		return render_template('index.html', data=data, status=status, maxlen=maxlen)
	return render_template('index.html', data=data, status=-1)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
	# print(current_app.root_path)
	# Appending app path to upload folder path within app root folder
	# uploads = os.path.join(current_app.root_path, "static\csv")
	# print(uploads)
	# Returning file from appended path
	return send_from_directory(directory=current_app.root_path, filename=filename, as_attachment=True)


if __name__ == "__main__":
	app.run(debug=True)
