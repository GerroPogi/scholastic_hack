import keyboard as k

keyBefore=None
pass
while True:
    key = k.read_key()
    print(key if keyBefore!=key else 0)
    keyBefore=key