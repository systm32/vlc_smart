import speech_recognition as sr

class sr_client:
    recog_obj = None
    def __init__(self):
        self.recog_obj = sr.Recognizer()
        
    def recognise(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.recog_obj.listen(source)
            
        try:
            return_val = self.recog_obj.recognize_google(audio);
            print("You said: " + return_val)
            return return_val
        except sr.UnknownValueError:
            print("Please Say again:")
            return "error"
        except sr.RequestError as e:
            print("Connection error,check your Connectivity; {0}".format(e))
            return "error"
    
s = sr_client();
s.recognise()