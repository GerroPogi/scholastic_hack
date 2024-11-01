import logging
import requests
from .settings import setting
from .window import Window
from .answerer import answer
import os
from bs4 import BeautifulSoup
import requests as r
from PIL import Image, ImageTk
from .utils import *

logging.basicConfig(filename="hack/logs/logs.log",datefmt='%m/%d/%Y %I:%M:%S %p',format='[%(levelname)s]: [%(asctime)s]: %(message)s',level=logging.DEBUG) # Development

# Checks if scholastic folder exists
logging.info('Checking if hack folder exists')
if not os.path.exists("hack"):
    os.mkdir("hack")

logging.info('Checking if scholastic folder exists')
if not os.path.exists("hack/scholastic"):
    os.mkdir("hack/scholastic")
    # SOON TO ADD: Image fetcher

logging.info('Checking if data exists')
if not os.path.exists("hack/data.json"):
    data = r.get("https://raw.githubusercontent.com/GerroPogi/scholastic_hack/draft1/hack/data.json")
    write(data.json(),"hack/data.json")

logging.info("fetched data.json")
data= read("hack/data.json")

def get_chat_models(tag):
    url= 'https://api.zukijourney.com/v1/models'
    page=requests.get(url)
    models=json.loads(BeautifulSoup(page.text,"html").text)['data']
    chat_models=[]
    for model in models:
        if model['type']=='chat.completions' and model['is_free']:
            chat_models.append(model[tag])
    return chat_models


def run():
    
    states={
        "active":True,
        "stage":0,
        "bgColor":"#2b2b28",
        "font":"Heebo Medium",
        "data":data,
        "chat_models":get_chat_models("id"),
        "scholastic":False # Checks if the hack is currently active
    }
    while states["active"]:
        if states["stage"] == 0:
            print("Going to mainpage")
            states = mainPage(states)
        if states["stage"] == 1:
            states = setting(states)
        if states["stage"]==2:
            states = answer(states)
            

def mainPage(states):
    def closer():
        nonlocal states
        states["active"]=False
        
        write(states["data"],"hack/data.json")
        
        mainPage.destroy()
    def switchState(state):
        nonlocal states
        mainPage.destroy()
        states["stage"]=state
    
    logging.info("Opening Main Page")
    mainPage = Window("500x500")
    data["screen_size"]=[mainPage.winfo_screenwidth(), mainPage.winfo_screenheight()] if not "screen_size" in data else data["screen_size"]
    logging.info("Added Screensize to the data var: %s" % data["screen_size"])
    
    mainPage.set_color("#2b2b28")
    mainPage.title("Scholastic Hack made by Beronicous")
    
    logo=Image.open("hack/logo.ico")
    logo =logo.resize([100,100])
    image = ImageTk.PhotoImage(logo)
    mainPage.add_label("logo","",image=image)
    
    mainPage.add_label("title","Welcome to the Scholastic Hack",font="impact 20",bg=states["bgColor"],fg="white")
    
    mainPage.add_button("settings","Settings",lambda: switchState(1),bg="#656659",fg="white",font=(states["font"],20))
    mainPage.add_button("settings","Start",lambda: switchState(2),bg="#656659",fg="white",font=(states["font"],20))
    mainPage.add_button("exit","Exit", closer,bg="#656659",fg="white",font=(states["font"],20))
    
    mainPage.add_label("info","For more information, check the github:","consolas 10",bg=states["bgColor"],fg="white")
    mainPage.add_label("link","https://github.com/GerroPogi/scholastic_hack","consolas 10",bg=states["bgColor"],fg="cyan",cursor="hand2")
    mainPage.get_widget("link").bind("<Button-1>", lambda e: callback("https://github.com/GerroPogi/scholastic_hack"))
    
    mainPage.run()
    return states