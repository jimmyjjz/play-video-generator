import json

with open("settings.json", "r") as f:
    data = json.load(f)

def set_setting(setting_name:str, value)->None:
    global data
    data[setting_name]=value

def get_setting(setting_name:str):
    return data[setting_name]

'''
def load_settings()->None:
    global data
    with open("settings.json","r") as f:
        data = json.load(f)
'''

def update_json()->None:
    with open("settings.json","w") as f:
        f.write(json.dumps(data, indent=2, sort_keys=False))

def default_settings()->None:
    global data
    data={
        "manual":False,
        "debug":0,#change to 0 when project not in development
        "horizontal":1080,
        "vertical":1920,
        "create_speech_fast":False
    }

# ==================================================TESTING==================================================
# set_setting("manual",False)