import json
import webbrowser

def callback(url):
    webbrowser.open_new(url)

def write(data, filename):
    print(type(data))
    with open(filename, 'w') as f:
        json.dump(data, f,indent=4)

def read(filename):
    return json.load(open(filename, 'r'))
