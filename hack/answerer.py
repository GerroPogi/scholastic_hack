from .window import Window


def answer(states):
    mainWin=Window("500x500")
    states["stage"]=0
    mainWin.title("Quiz Answerer of Scholastic Hack")
    mainWin.set_color(states["bgColor"])
    
    
    
    mainWin.run()
    return states