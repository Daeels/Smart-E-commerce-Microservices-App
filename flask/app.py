# Importing librairies


from flask import *
import simpleaudio as sa
import os
import speech_recognition as sr
import requests


app = Flask(__name__)

@app.route('/get_the_voice', methods=["POST"])
def get_the_voice():

    # Get the voice from client
    #app.logger.debug(request.files['sound'].filename)
    recieved_sound = request.files['sound']
    file_name = "recieved_sound.wav"
    recieved_sound.save(file_name)
    
    print("sound recieved, applying speech recognition...")






    r = sr.Recognizer()
    with sr.AudioFile(file_name) as source :
    	audio = r.record(source)

    txt = r.recognize_google(audio,language="fr-FR")

  




    
    data = {'speech' : txt}
    URL = "http://127.0.0.1:5001/client"



    print("speech recognized, sending to the other server...")
    response = requests.post(URL, json=data)
	


    print(response.text)








    # wave_obj = sa.WaveObject.from_wave_file(file_name)
    # play_obj = wave_obj.play()
    # play_obj.wait_done
    os.remove(file_name)
    
    return 'recieved'
    # Make speech to text


    # Send the text to Spring



    







# Run the app

if __name__ == '__main__':
    app.run(debug=True)