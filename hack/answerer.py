from .window import Window
import keyboard as k


def answer(states):
    # TODO make states["scholastic"] be true when it starts
    keyBefore=None
    def stop_listener():
        while True:
            nonlocal keyBefore
            
            key=k.read_key()
            if [keyBefore,key]==states["data"]["hotkey"]:
                states["scholastic"]=False
            keyBefore=key if keyBefore!=key else keyBefore
        
    mainWin=Window("500x500")
    states["stage"]=0
    mainWin.title("Quiz Answerer of Scholastic Hack")
    mainWin.set_color(states["bgColor"])
    
    
    
    mainWin.run()
    return states