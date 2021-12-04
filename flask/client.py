# #request object : https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# from flask import Flask, request
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# CORS(app)

# @app.route('/client', methods=["POST"])
# def client():
# 	print("request recieved")
# 	# speech = request.json['speech']
# 	# print(speech)
# 	print(request.files['sound']) 
# 	return 'recieved'


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', debug=True, port=5001)
