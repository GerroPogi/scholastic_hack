import logging
from openai import APIStatusError, OpenAI, PermissionDeniedError

def check_api_key(key:str):
    success=False
    errorCode=0
    try:
        chatgpt=OpenAI(api_key=key,base_url="https://zukijourney.xyzbot.net/v1")
        response = chatgpt.chat.completions.create(
            model="caramelldansen-1", # or gpt-4o-mini, claude-3-haiku, gemini-1.5-flash, etc...
            messages=[{"role": "user", "content": "Hello, AI!"}]
        )
        logging.error("Tried to put the key: "+key+". The API returned no error because the key is valid. Returning true.")
        success=True
    except PermissionDeniedError as e:
        errorCode=2
        logging.error("Tried to put the key: "+key+". The API returned an error because the key is in another IP. Returning false.")
    except APIStatusError as e:
        errorCode=1
        logging.error("Tried to put the key: "+key+". The API returned an error because the key is invalid. Returning false.")
    
    except Exception as ex:
        template = "An exception inside checking api key. Type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        errorCode=3
        logging.info(message)
    
    return success, errorCode
    # TODO Add another except when the key has no more credits