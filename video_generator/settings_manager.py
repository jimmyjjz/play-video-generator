import json
def change_setting(setting_name:str, value)->None:
    with open("settings.json","r") as f:
        data = json.load(f)
    with open("settings.json","w") as f:
        data[setting_name]=value
        f.write(json.dumps(data, indent=2, sort_keys=False))

# ==================================================TESTING==================================================
change_setting("manual",False)