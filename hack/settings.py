from .window import Window


def setting(states):
    mainWin=Window("500x500")
    states["stage"]=0
    mainWin.title("Settings of Scholastic Hack")
    mainWin.set_color(states["bgColor"])
    
    mainWin.add_box("readerBox",[400,200],color="#706463",pos=[50,10])
    
    mainWin.get_widget("readerBox").add_label("title","Reader Options",pos=[100,10],bg="#706463",font=(states["font"],20),fg="white")
    mainWin.get_widget("readerBox").add_label("delayText","Delay Time (seconds)",pos=[10,60],font=(states["font"],10),bg="#706463",fg="white")
    mainWin.get_widget("readerBox").add_scale("delay",20,500,60,pos=[150,50],width=10,length=200,bg="#706463",fg="white")
    mainWin.get_widget("readerBox").add_checkbox("2pager","2-Page Mode",False,pos=[10,90],font=(states["font"],10),bg="#706463",fg="white")
    
    mainWin.run()
    return states