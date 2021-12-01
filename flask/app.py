# Importing librairies
#Stackoverflow question about the same issue we're facing : https://stackoverflow.com/questions/61466799/docker-failed-to-establish-a-new-connection-errno-111-connection-refused


from flask import *
#import simpleaudio as sa
import os
from SpeechRecognizer import SpeechRecognizer
import requests


app = Flask(__name__)

@app.route('/get_the_voice', methods=["GET"])
def get_the_voice():

    # Get the voice from frontend
    recieved_sound = request.files['sound']
    file_name = "recieved_sound.wav"
    recieved_sound.save(file_name)
    
    
    #Transform speech to text
    print("sound recieved, applying speech recognition...")
    sr = SpeechRecognizer("fr-FR")
    txt = sr.recognize(file_name)



    #Send recognized text to backend and print the response
    print("speech recognized, sending to the other server...")
    data = {'speech' : txt}
    URL = "http://0.0.0.0:5001/client"
    response = requests.get(URL, json=data)
    print(response.text)


    #Delete sound file
    os.remove(file_name)


	#Send response to the frontend
    return 'recieved'
    #return txt


# Run the app

if __name__ == '__main__':
    app.run(host='127.0.0.0', port=5000, debug=True)