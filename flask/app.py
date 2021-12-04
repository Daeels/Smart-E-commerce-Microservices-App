# In this version, An attempt to convert to blob object to base64 before sending it to the server,
# the server then converts it back to wav format.
# Issue faced : audio is in reality recieved in webm format, and a method to convert it to pcm wav is still ambigious.
# When the webm recieved file is converted using a web tool (https://cloudconvert.com/webm-to-wav),
# the resulting file works fine in the speech recognizer.
# Tool to check the real format of a file : https://www.checkfiletype.com/ 
# Succeded to convert webm to wav with ffmpeg



from flask import Flask, request
from flask_cors import CORS, cross_origin
from SpeechRecognizer import SpeechRecognizer
import requests
import base64
import ffmpeg
import os

app = Flask(__name__)
CORS(app)

@app.route('/get_the_voice', methods=["GET"])
def get_the_voice():

    
    # print(request.json['sound'])
    #Get the voice from frontend 1
    # print(request.json)

    decoded_data = base64.b64decode(request.json['sound'], '+/')
    # print(decoded_data)
    wav_file = open("temp.webm", "wb")
    wav_file.write(decoded_data)
    wav_file.close()

    #webm to wav
    # command = ['./FFmpeg/bin/ffmpeg', '-i', 'temp.webm', '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000', 'temp' + '.wav']
    # subprocess.run(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE)

    try:
        ffmpeg.input('temp.webm') \
            .output('temp.wav') \
            .run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
    


    
    #Transform speech to text
    print("sound recieved, applying speech recognition...")
    sr = SpeechRecognizer("fr-FR")

    try:
        txt = sr.recognize("temp.wav")
        print(txt)
    except Exception as e:
        print(e)
        print("could not recognize the speech")
        

    # Send recognized text to backend and print the response
    print("speech recognized, sending to the other server...")
    # data = {'speech' : txt}
    # txt = "Nike Jordan noir"
    URL = "http://127.0.0.1:8080/products/search/findByDescription?keyword="+txt
    response = requests.get(URL)
    json = response.json()


    #Delete sound file
    os.remove('temp.webm')
    os.remove('temp.wav')

    #Send response to the frontend
    return 'recieved'
    #return txt


# Run the app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)