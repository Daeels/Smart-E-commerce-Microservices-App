import ffmpeg
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/ecommerce_microservices'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
base = automap_base()
base.prepare(db.engine, reflect=True)
product = base.classes.product
category = base.classes.category


@app.route('/test_ffmepg', methods=["GET"])
def test_ffmepg():
	try:
		ffmpeg.input('temp.webm') \
			.output('temp.wav') \
			.run(capture_stdout=True, capture_stderr=True)
		return 'l7wa'
	except ffmpeg.Error as e:
		print('stdout:', e.stdout.decode('utf8'))
		print('stderr:', e.stderr.decode('utf8'))
		raise e
		return 'mal7wach'

	



@app.route('/test_db', methods=["GET"])
def test_db():
	products_descriptions = db.session.query(product.description)
	for product_description in products_descriptions:
		print(product_description)
	return 'l7wa'


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000, debug=True)