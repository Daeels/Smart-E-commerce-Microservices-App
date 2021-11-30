from flask import *


app = Flask(__name__)

@app.route('/client', methods=["POST"])
def client():
	print("request recieved")
	speech = request.json['speech']
	print(speech)
	return 'recieved'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
