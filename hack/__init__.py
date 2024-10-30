from .window import Window
import os
import requests as r
from utils import *

# Checks if scholastic folder exists
if not os.path.exists("hack"):
    os.mkdir("hack")

if not os.path.exists("hack/scholastic"):
    os.mkdir("hack/scholastic")
    # SOON TO ADD: Image fetcher

if not os.path.exists("hack/data.json"):
    data = r.get("https://raw.githubusercontent.com/GerroPogi/scholastic_hack/draft1/hack/data.json")
    write(data.json())
data= read("hack/data.json")

def run():
    mainWin = Window("1000x1000")
    
    
    mainWin.run()