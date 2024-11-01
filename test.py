import keyboard as k
# TODO: DELETE THIS WHEN YOU PUBLISH
keyBefore=None
pass
while True:
    key = k.read_key()
    print(key if keyBefore!=key else 0)
    keyBefore=key