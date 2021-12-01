#this class is to hold the recognizer

import speech_recognition as sr

class SpeechRecognizer:
    
    def __init__(self, language):
        self.recognizer = sr.Recognizer()
        self.language = language


    def recognize(self, file_name):
        with sr.AudioFile(file_name) as source :
            audio = self.recognizer.record(source)

        txt = self.recognizer.recognize_google(audio, language=self.language)
        return txt
