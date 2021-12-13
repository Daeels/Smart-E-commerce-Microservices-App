# In this version, An attempt to convert to blob object to base64 before sending it to the server,
# the server then converts it back to wav format.
# Issue faced : audio is in reality recieved in webm format, and a method to convert it to pcm wav is still ambigious.
# When the webm recieved file is converted using a web tool (https://cloudconvert.com/webm-to-wav),
# the resulting file works fine in the speech recognizer.
# Tool to check the real format of a file : https://www.checkfiletype.com/ 
# Succeded to convert webm to wav with ffmpeg
# sudo apt install ffmpeg


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from SpeechRecognizer import SpeechRecognizer
import requests
import base64
import ffmpeg
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/ecommerce_microservices'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
base = automap_base()
base.prepare(db.engine, reflect=True)
product = base.classes.product
category = base.classes.category

@app.route('/search-by-voice', methods=["POST"])
def search_by_voice():
   
    # Get the voice recorded by the user and write it into a webm file
    decoded_data = base64.b64decode(request.json['sound'], '+/')
    wav_file = open("temp.webm", "wb")
    wav_file.write(decoded_data)
    wav_file.close()

    #webm to wav
    # command = ['./FFmpeg/bin/ffmpeg', '-i', 'temp.webm', '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', 'temp' + '.wav']
    # subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

    # Convert webm file to wav file
    try:
        ffmpeg.input('temp.webm') \
            .output('temp.wav') \
            .run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))

        try:
            os.remove('temp.webm')
        except OSError:
            pass
        try:
            os.remove('temp.wav')
        except OSError:
            pass

        return "Le programme a rencontré une erreur de conversion de voix, veuillez reessayer.", 500
    


    
    #Transform speech recorded to text using the wav file
    print("sound recieved, applying speech recognition...")
    sr = SpeechRecognizer("fr-FR")

    try:
        recognized_speech = sr.recognize("temp.wav")
        # print(recognized_speech)
    except Exception as e:
        print(e)
        print("could not recognize the speech")
        return "Votre discours n'a pas ete reconnu, veuillez reessayer.", 400
        

    # Send recognized text to backend and print the response
    print("speech recognized, you said : "+recognized_speech+", fetching products...")
    
    # Get all the products' descriptions from the database, and delete the second element from the tuple returned
    products_descriptions = db.session.query(product.description)
    products_descriptions = [product_description[0] for product_description in products_descriptions]

    # Join the text typed by the user to all the descriptions of products to vectorize them
    all_tokens = [recognized_speech] + products_descriptions
    # Create a vectorizer
    vectorizer = CountVectorizer()
    # Transform the text using the vectorizer
    vector = vectorizer.fit_transform(all_tokens)

    # Transform the vectors to an array
    array = vector.toarray()
    
    
    # Create a dictionnary holding the distances between each product description and the text typed by the user
    distances = {}
    for i in range(1, len(all_tokens)):
        # distances.append({all_tokens[i]: euclidean_distances([array[i]], [array[0]])[0][0]})
        distances[all_tokens[i]] = cosine_similarity([array[i]], [array[0]])[0][0]

    # Sort the distances and delete distances that equals
    sorted_distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
    sorted_distances = {key:value for key,value in sorted_distances.items() if value!=0}
    
    # Place 1/3 of the descriptions with the smallest distance in a variable
    most_suitable_descriptions = list(sorted_distances.keys())
    
    # Place the chosen products in a json object
    products_selected_json = []
    for suitable_description in most_suitable_descriptions :
        # products_selected.append(db.session.query(product).filter(product.description == suitable_description))
        products_querried = db.session.query(product).filter(product.description == suitable_description).all()
        for product_querried in products_querried:
            products_selected_json.append({'name':product_querried.name, 'id':product_querried.id, 'available':product_querried.available, 'current_price':product_querried.current_price, 'description':product_querried.description, 'photo_name':product_querried.photo_name, 'promotion':product_querried.promotion, 'selected':product_querried.selected, 'category_id':product_querried.category_id})
        
        
    products_selected_json = {"_embedded" : {"products" : products_selected_json}}
    products_selected_json = jsonify(products_selected_json)


 
    #Delete sound file
    try:
        os.remove('temp.webm')
    except OSError:
        pass
    try:
        os.remove('temp.wav')
    except OSError:
        pass

    # Send the products back to the client
    return products_selected_json
    





@app.route('/search-by-text', methods=["GET"])
def search_by_text():

    # Get the text typed by the user
    queried_text = request.args.get('text')
    
    # Check if the text typed by tse user is not empty
    if queried_text != '':

        # Get all the products' descriptions from the database, and delete the second element from the tuple returned
        products_descriptions = db.session.query(product.description)
        products_descriptions = [product_description[0] for product_description in products_descriptions]

        # Join the text typed by the user to all the descriptions of products to vectorize them
        all_tokens = [queried_text] + products_descriptions
        # Create a vectorizer
        vectorizer = CountVectorizer()
        # Transform the text using the vectorizer
        vector = vectorizer.fit_transform(all_tokens)
        # Transform the vectors to an array
        array = vector.toarray()
        
        
        # Create a dictionnary holding the distances between each product description and the text typed by the user
        distances = {}
        for i in range(1, len(all_tokens)):
            distances[all_tokens[i]] = cosine_similarity([array[0]], [array[i]])[0][0]

        # Sort the distances and remove the distances that equals to 0
        sorted_distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1], reverse=True)}
        sorted_distances = {key:value for key,value in sorted_distances.items() if value!=0}
        print(sorted_distances)

        # Place 1/3 of the descriptions with the smallest distance in a variable
        most_suitable_descriptions = list(sorted_distances.keys())

        # print(most_suitable_descriptions)

        # :int(ceil(len(distances)/3))
        
        # Place the chosen products in a json object
        products_selected_json = []
        for suitable_description in most_suitable_descriptions :
            # products_selected.append(db.session.query(product).filter(product.description == suitable_description))
            products_querried = db.session.query(product).filter(product.description == suitable_description).all()
            for product_querried in products_querried:
                products_selected_json.append({'name':product_querried.name, 'id':product_querried.id, 'available':product_querried.available, 'current_price':product_querried.current_price, 'description':product_querried.description, 'photo_name':product_querried.photo_name, 'promotion':product_querried.promotion, 'selected':product_querried.selected, 'category_id':product_querried.category_id})
            
            
        products_selected_json = {"_embedded" : {"products" : products_selected_json}}
        products_selected_json = jsonify(products_selected_json)

        # Send the json object containing the products back to the client
        return products_selected_json

    else:
        return 'Veuillez ecrire quelque chose', 500

# Run the app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)