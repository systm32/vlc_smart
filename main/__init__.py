import sys, os, subprocess, importlib, time, socket, threading

flag = 1

class vlc_smart:
    
    bool_vlc = True
    bool_pip = True
    
    def __init__(self):
        
        # checking if vlc exists
        try:
            print("Checking if VLC exists")
            subprocess.call(["vlc", "--version"])
        except:
            print("VLC not found\nTO install vlc type\n$ sudo apt-get install vlc")
            self.bool_vlc = False
            
        # checking if pip exists
        try:
            print("Checking if PIP exists")
            subprocess.call(["pip", "--version"])
        except:
            print("PIP not found\nTo install pip type\n$sudo apt-get install python-pip")
            self.bool_pip = False
        
        # exit if anyone's missing
        if self.bool_vlc == False or self.bool_pip == False:
            exit(0)
        
        # install and import
        vlc_smart.install_and_import(self, "pyaudio")
        vlc_smart.install_and_import(self, "speech_recognition")       
        print("Explicit dependencies statisfied!")
        
        # check if microphone is attached
        try:
            num_micros = len(globals()["speech_recognition"].Microphone.list_microphone_names());
            if(num_micros == 0):
                num_micros = num_micros / 0
            print("Microphone Found!");
        except Exception as e:
            print("Some Error Occured while Searching for Microphones\nPlease make Sure you have Microphones attached");   
            
    def install_and_import(self, package):
        try:
            print("Checking if " + package + " exists")
            importlib.import_module(package)
            print("Satisfied!")
        except ImportError:
            print("Installing Package, may take some time")
            import pip
            pip.main(['install', package])
        finally:
            if(package == "speechrecognition"):
                package = "speech_recognition"
            globals()[package] = importlib.import_module(package)
    
class vlc_client:
    port = "4200"
    socket_object = None
    socket_connected = False
    wait_time = 50
    
    def __init__(self, port=4200, default_playlist=""):
        self.port = port
        
        try:
            t = threading.Thread(target=self.vlc_process, args=(port, default_playlist))
            t.start()
        except:
            print("Error hosting vlc on said port. Try changing socket port in settings")
            exit(0) 
        
        disp_once = False
        while True:
            try:
                self.socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_object.connect(('localhost', port))
                print("Connected")
                self.socket_connected = True
                break
            except:
                if(disp_once == False):
                    print("Trying to Connect")
                    disp_once = True
        
    def vlc_process(self, the_port=4200, playlist=""):
        os.system("vlc --extraintf rc --rc-host localhost:" + the_port.__str__() + " " + playlist)     
        
    def play(self):
        new_time = time.time()
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "play\n"
        print("Playing")
        self.socket_object.sendall(cmd.encode())
    
    def pause(self):
        new_time = time.time()
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "pause\n"
        print("Pausing")
        self.socket_object.sendall(cmd.encode())
    
    def next(self):
        new_time = time.time()
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "next\n"
        print("Playing Next")
        self.socket_object.sendall(cmd.encode())
    
    def previous(self):
        new_time = time.time()
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "prev\n"
        print("Playing Previous")
        self.socket_object.sendall(cmd.encode())
    
    def stop(self):
        new_time = time.time();
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "stop\n"
        print("Stopped")
        self.socket_object.sendall(cmd.encode()) 

class sr_client:
    recog_obj = None
    def __init__(self):
        self.recog_obj = globals()["speech_recognition"].Recognizer()
        
    def sound_recognise(self):
        global flag
        try:
            with globals()["speech_recognition"].Microphone() as source:
                print("Your Command:")
                audio = self.recog_obj.listen(source)
            print audio
            return_val = "error"
            return_val = self.recog_obj.recognize_google(audio)
            flag = 1
            print("You said: " + return_val)            
        except globals()["speech_recognition"].UnknownValueError:
            flag = 1
            print("Please Say again:")            
        except globals()["speech_recognition"].RequestError as e:
            flag = 1
            print("Connection error,check your Connectivity;\n {0}".format(e))    
        except Exception as e:
            flag = 1
            print("Some error Occured...Continue...")        
        flag = 1
        return return_val

def main():
    enough = False
    try:
        vlc_smart()
    except Exception as e:
        print("Error Occured")
    finally:
        vc = vlc_client(port = 4200, default_playlist="pk.xspf")
        sr = sr_client()
        global flag;
        while(True):
            print 'Hey'
            if flag == 1:
                flag = 0
                word = sr.sound_recognise()
                if(word == "activate"):
                    enough = False
                if word == "enough":
                    enough = True   
                if(enough == True):
                    continue       
                if word == "play":
                    vc.play()
                if word == "hold" or word == "old" or word == "cold" or word == "told" or word =="pause" or word == "p***":
                    vc.pause()
                if word == "next":
                    vc.next()
                if word == "previous":
                    vc.previous()   
                if word == "stop":
                    vc.stop()
            
main()
