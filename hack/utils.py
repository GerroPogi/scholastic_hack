import json

def write(data, filename):
    json.dump(data, open(filename, 'wb'),indent=4)

def read(filename):
    return json.load(open(filename, 'r'))