from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

@app.route('/flaskClient1', methods=["POST"])
def flaskClient1():

	response = requests.get('http://0.0.0.0:5001/client')
	return(response.text)





if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)