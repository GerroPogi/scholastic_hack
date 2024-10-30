from .window import Window
import os

# Checks if scholastic folder exists
if not os.path.exists("hack"):
    os.mkdir("hack")

if not os.path.exists("hack/scholastic"):
    os.mkdir("hack/scholastic")
    # SOON TO ADD: Image fetcher

if not os.path.exists("hack/data.json"):
    

def run():
    mainWin = Window("1000x1000")
    
    
    mainWin.run()