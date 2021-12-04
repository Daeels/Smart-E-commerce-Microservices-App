# Importing librairies
#Stackoverflow question about the same issue we're facing in docker compose: https://stackoverflow.com/questions/61466799/docker-failed-to-establish-a-new-connection-errno-111-connection-refused
#type of sound recieve : werkzeug.FileStorage -> application/octet-stream
#Next piste : recorder.js and type: "audio/wav" and https://www.geeksforgeeks.org/how-to-convert-blob-to-base64-encoding-using-javascript/

from flask import Flask, request
from flask_cors import CORS, cross_origin
import simpleaudio as sa
import os
from SpeechRecognizer import SpeechRecognizer
import requests
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import base64
import wave

app = Flask(__name__)
CORS(app)

@app.route('/get_the_voice', methods=["POST"])
def get_the_voice():

    
    #Get the voice from frontend 1
    # print(request.json)

    decoded_data = base64.b64decode(request.json['sound'], '+/')
    # print(decoded_data)
    wav_file = open("temp.wav", "wb")
    wav_file.write(decoded_data)
    wav_file.close()






    # Get the voice from frontend
    # recieved_sound = request.files['sound']
    # print(recieved_sound)
    # file_name = "recieved_sound.wav"
    # # recieved_sound.save(file_name)
    # # print(request.headers['Content-Type'])
    
    

    #Play the sound
    # wave_obj = sa.WaveObject.from_wave_file(file_name)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()



    
    #Transform speech to text
    print("sound recieved, applying speech recognition...")
    sr = SpeechRecognizer("fr-FR")

    try:
        txt = sr.recognize("temp.wav")
        print(txt)
    except Exception as e:
        print(e)
        # print("could not recognize the speech")
        

    #Send recognized text to backend and print the response
    # print("speech recognized, sending to the other server...")
    # data = {'speech' : txt}
    # URL = "http://0.0.0.0:5001/client"
    # response = requests.get(URL, json=data)
    # print(response.text)


    #Delete sound file
    # os.remove(file_name)


    #Send response to the frontend
    return 'recieved'
    #return txt


# Run the app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)