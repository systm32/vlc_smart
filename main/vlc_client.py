import threading
import subprocess
import socket
import os
import time

class vlc_client:
    port = "4200"
    socket_object = None
    socket_connected = False
    wait_time = 500
    
    def __init__(self,port = 4200,default_playlist = ""):
        self.port = port
        
        try:
            t = threading.Thread(target = self.vlc_process, args=(port,default_playlist))
            t.start()
        except:
            print("Error hosting vlc on said port. Try changing socket port in settings")
            exit(0);           
        
        disp_once = False;
        while True:
            try:
                self.socket_object = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.socket_object.connect(('localhost',port))
                print("Connected")
                self.socket_connected = True;
                break
            except:
                if(disp_once == False):
                    print("Trying to Connect")
                    disp_once = True
        
    def vlc_process(self,the_port = 4200,playlist=""):
        os.system("vlc --extraintf rc --rc-host localhost:"+the_port.__str__()+" "+playlist);        
        
    def play(self):
        new_time = time.time();
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "play\n"
        print("Playing")
        self.socket_object.sendall(cmd.encode())
    
    def pause(self):
        new_time = time.time();
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "pause\n"
        print("Pausing")
        self.socket_object.sendall(cmd.encode())
    
    def next(self):
        new_time = time.time();
        while True:
            if(time.time() - new_time > self.wait_time):
                break            
            if self.socket_connected:
                break
        cmd = "next\n"
        print("Playing Next")
        self.socket_object.sendall(cmd.encode())
    
    def previous(self):
        new_time = time.time();
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

#Testing values
# vlc = vlc_client(default_playlist="pk.xspf");
# time.sleep(10)
# vlc.pause()
# time.sleep(3)
# vlc.play()
# time.sleep(3)
# vlc.pause()
# time.sleep(3)
# vlc.play()
