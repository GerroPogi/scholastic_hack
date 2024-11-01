import logging
from threading import Thread
import keyboard

from .utils import callback

from .chat import check_api_key
from .window import Box, Window,DraggableBox

def format_hotkey(hotkey):
    formatedKeys=""
    for i,key in enumerate(hotkey):
        formatedKeys+=key.title()+("+" if not (i==len(hotkey)-1) else "")
    return formatedKeys

def setting(states):
    mainWin=Window("500x600")
    states["stage"]=0
    mainWin.title("Settings of Scholastic Hack")
    mainWin.set_color(states["bgColor"])
    readerData=states["data"]["reader"]
    
    # Reader Option Section
    mainWin.add_box("reader-box",[400,150],color="#706463",pos=[50,10])
    
    readerBox:Box=mainWin.get_widget("reader-box")
    readerBox.add_label(
        "title",
        "Reader Options",
        pos=[100,10],
        bg="#706463",
        font=(states["font"],20),
        fg="white"
        )
    readerBox.add_label(
        "delayText",
        "Delay Time (seconds)",
        pos=[10,60],
        font=(states["font"],10),
        bg="#706463",
        fg="white"
        )
    readerBox.add_scale(
        "delay",
        20,
        500,
        readerData["delay"],
        pos=[150,50],
        width=10,
        length=200,
        bg="#706463",
        fg="white",
        command=lambda val: readerData.update({"delay":int(val)})
        )
    readerBox.add_checkbox(
        "2pager",
        "2-Page Mode",
        readerData["2-page-mode"],
        pos=[50,100],
        font=(states["font"],10),
        bg="#ccb8b9",
        command=lambda: states["data"]["reader"].update({"2-page-mode":readerBox.get_widget("2pager")[1].get()}),
        )
    readerBox.add_button(
        "boxes",
        "Adjust Box Settings",
        lambda: states.update(readerBoxes(mainWin,states)),
        font=(states["font"],10),
        pos=[210,100],
        width=20,
        bg="#ccb8b9"
        )
    
    # Quiz Answerer Option Section
    mainWin.add_box("answerer-box",[400,150],color="#706463",pos=[50,200])
    
    answerBox:Box=mainWin.get_widget("answerer-box")
    answerBox.add_label(
        "title",
        "Quiz Answerer Options",
        pos=[50,10],
        bg="#706463",
        font=(states["font"],20),
        fg="white"
    )
    answerBox.add_dropdown(
        "models",
        states["data"]["answerer"]["model"],
        states["chat_models"],
        pos=[50,70],
        font=(states["font"],10),
        bg="#ccb8b9",
        fg="black",
        )
    
    answerBox.add_button(
        "boxes",
        "Adjust Box Settings",
        lambda: answerBoxes(mainWin,states),
        font=(states["font"],10),
        pos=[210,70],
        width=20,
        bg="#ccb8b9"
    )
    
    # Other options section
    mainWin.add_box("others-box",[400,150],"#706463",[50,400])
    othersBox:Box=mainWin.get_widget("others-box")
    othersBox.add_label(
        "title",
        "Others",
        font=(states["font"],20),
        pos=[150,10],
        bg="#706463",
        fg="white"
        )
    
    # Hot key handling
    othersBox.add_label(
        "hotkey",
        f"Hotkey: {format_hotkey(states["data"]["hotkey"])}" ,
        pos=[10,50],
        bg="#706463",
        fg="white",
        font=(states["font"],15)
    )
    
    def set_new_key():
        othersBox.get_widget("hotkey").configure(text="Waitin for hotkey")
        mainWin.update()
        new_hotkey=[]
        keyBefore=None
        while True:
            key = keyboard.read_key()
            new_hotkey.append(key) if key!=keyBefore else 0
            keyBefore=key if keyBefore!=key else keyBefore
            
            othersBox.get_widget("hotkey").configure(text=f"Waitin for hotkey: {format_hotkey(new_hotkey)}")
            mainWin.update()
            
            if len(new_hotkey)>=2:
                break
            
        logging.info("Made a new hotkey: {0}".format(new_hotkey))
        othersBox.get_widget("hotkey").configure(text=f"Hotkey: {format_hotkey(new_hotkey)}")
        mainWin.update()
        
    
    othersBox.add_button(
        "hotkey-button",
        "Set new hotkey",
        lambda: Thread(target=set_new_key).start(),
        font=(states["font"],10),
        bg="#ccb8b9",
        pos=[10,100],
        width=20,
        height=1
    )
    
    # Getting key
    othersBox.add_label(
        "api-key-title",
        "API Key",
        font=(states["font"],10),
        pos=[200,50],
        bg="#706463",
        fg="white"
    )
    
    othersBox.add_entry(
        "api-key",
        default_entry=states["data"]["api-key"],
        font=(states["font"],15),
        pos=[200,80],
        width=7,
    )
    
    def check_if_valid_key():
        api_entry=othersBox.get_widget("api-key").get()
        valid= check_api_key(api_entry)
        if valid[0]:
            othersBox.get_widget("api-key-title").configure(text="API key - Valid",fg="lawn green")
        else:
            othersBox.get_widget("api-key-title").configure(text="API key -"+("Invalid key" if valid[1]==1 else "Invalid IP" if valid[1]==2 else "Unknown Error"),fg="indianred1")
            
    
    othersBox.add_button(
        "check-api",
        "Check key",
        lambda: Thread(target=check_if_valid_key).start(),
        font=(states["font"],10),
        bg="#ccb8b9",
        pos=[300,80]
    )
    
    othersBox.add_label(
        "api-instructions",
        "How to get your API Key",
        "consolas 10",
        bg="#706463",
        fg="cyan",
        cursor="hand2",
        pos=[200,120]
        )
    othersBox.get_widget("api-instructions").bind("<Button-1>", lambda e: callback("https://github.com/GerroPogi/scholastic_hack/tree/draft1#how-to-get-api-key"))
    
    def onClose():
        nonlocal states
        states["data"]["answerer"].update({"model":answerBox.get_widget("models")[1].get()}) # Because dropdown has no command argument
        states["data"]["api-key"]=othersBox.get_widget("api-key").get() # Because entry has no command argument
        mainWin.destroy()
        return states
    
    mainWin.protocol("WM_DELETE_WINDOW",onClose)
    
    mainWin.run()
    
    return states

def readerBoxes(master,states):
    """The popup for the boxes when you click to adjust box settings for reader

    Args:
        master (hack.Window): The settings window that it originated. To be minimized
        states (dict): The states that are passed around the program
    """
    def onClose():
        master.deiconify()
        if readerData["2-page-mode"]:
            states["data"]["reader"].update({
                "size":size,
                "page1":page1.new_pos,
                "page2":page2.new_pos
            })
        else:
            states["data"]["reader"].update({
                "size":size,
                "page":page.new_pos
            })
        mainWin.destroy()
        return states
    def updateSize():
        nonlocal size
        size=mainWin.get_widget("size").get()
        print(size)
        if readerData["2-page-mode"]:
            page1.configure(width=250*size,height=300*size)
            page2.configure(width=250*size,height=300*size)
            
            page1.packs()
            page2.packs()
        else:
            page.configure(width=250*size,height=300*size)
            page.packs()
        
    
    master.iconify()
    
    readerData=states["data"]["reader"]
    screenSize=states["data"]["screen_size"]
    mainWin=Window(str(screenSize[0])+"x"+str(screenSize[1]))
    mainWin.set_color(states["bgColor"])
    mainWin.set_alpha(0.5)
    mainWin.protocol("WM_DELETE_WINDOW",onClose)
    
    # Size Scale
    mainWin.add_scale("size",1,10,readerData["size"])
    size=mainWin.get_widget("size").get()
    
    if readerData["2-page-mode"]:
        # Left book page
        page1=DraggableBox([250*readerData["size"],300*readerData["size"]],master=mainWin,color="#c2b2b2",pos=readerData["page1"])
        page1.add_label("text","Left page",pos=[10,10])
        
        # Right book page
        page2=DraggableBox([250*readerData["size"],300*readerData["size"]],master=mainWin,color="#e8d5d5",pos=readerData["page2"])
        page2.add_label("text","Right page",pos=[10,10])
        
        page1.packs()
        page2.packs()
    
    else: # For only 1 page reading (inefficient)
        page=DraggableBox([250*readerData["size"],300*readerData["size"]],master=mainWin,color="#c2b2b2",pos=readerData["page"])
        page.packs()
        
    
    # Updater
    mainWin.add_button("update-size","Update Size",updateSize)
    
    mainWin.run()
    return states

def answerBoxes(master,states):
    """The popup for the boxes when you click to adjust box settings for quiz answerer

    Args:
        master (hack.Window): The settings window that it originated. To be minimized
        states (dict): The states that are passed around the program
    """
    def onClose():
        master.deiconify()
        states["data"]["answerer"]={
            "size":size,
            "question":questionBox.new_pos,
            "book": bookBox.new_pos,
        }
        for key,value in choices.items():
            states["data"]["answerer"][key]=value.new_pos
        
        mainWin.destroy()
        return states
    def update():
        nonlocal size
        size=mainWin.get_widget("size").get()
        for value in choices.values():
            value.configure(width=60*size,height=15*size)
        
    master.iconify()
    
    screensize=states["data"]["screen_size"]
    mainWin=Window(str(screensize[0])+"x"+str(screensize[1]))
    mainWin.set_alpha(0.5)
    mainWin.protocol("WM_DELETE_WINDOW",onClose)
    
    
    answererData=states["data"]["answerer"]
    
    

    bookBox=DraggableBox(size=[screensize[0]/2,70],color="#767a5d",master=mainWin,pos=answererData["book"])
    bookBox.add_label("text","Book",pos=[10,10])
    
    
    questionBox=DraggableBox([screensize[0]-10,150],color="#767a5d",master=mainWin,pos=answererData["question"])
    questionBox.add_label("text","Question",pos=[10,10])
    
    choices={}
    size=answererData["size"]
    for i,choice in enumerate("acbd"):
        choices[choice]=DraggableBox(pos=answererData[choice],size=[60*size,15*size],color='#%02x%02x%02x' % (10*(i+1), 10*(i+1), 10*(i+1)),master=mainWin)
        choices[choice].add_label("text",choice.upper()+".",pos=[10,10])
        
        choices[choice].packs()
        
    bookBox.packs()
    questionBox.packs()
    
    # Size scale
    mainWin.add_scale(
        "size",
        1,
        20,
        answererData["size"]
        )
    print(mainWin.get_widget("size").get())
    
    
    # Size updater
    mainWin.add_button("updater","Update Size",update)
    
    mainWin.run()
    return states