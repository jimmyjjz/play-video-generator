def check_script(script:str):#not entirely accurate name as it replaces GPT ' with regular '(this means does more than just check)
    print(script)
    print("Checking script...")
    #DOUBLE CHECK TO SEE IF IT IS ALL GONE(THIS COMMENT MIGHT GET DELETED IN THE FUTURE)
    if "â€™" in script:
        raise ValueError("GPT apostrophe found in script")
    if "Ã©" in script:
        raise ValueError("Accented e found in script. Check for cafe with accented e in script.")
    splitted=script.split("|")
    characters=splitted[1].split(",")
    names=[]
    emotion_slot=['thinking', 'ok', 'sad', 'angry', 'has_emotion_but_no_emoji_popup']
    throwables=['attack','mail','tree']
    throw_speeds=['fast','slow']
    fc,mc=0,0
    for c in characters:
        s=c.split("-")
        names.append(s[1])
        if s[0]=='male':
            mc+=1
        elif s[0]=='female':
            fc+=1
        else:
            print(s[0])
            raise ValueError("A Character's gender is not supported")
    if mc > 5:
        print("Male count:", fc)
        raise ValueError("Too much males")
    if fc > 5:
        print("Female count:",fc)
        raise ValueError("Too much females")
    characters_in_scene=[]
    for v in splitted[2:]:
        s=v.split("-")
        match len(s):
            case 1:#d
                s2=s[0].split(":")
                if len(s2)!=3:
                    print(s)
                    raise ValueError("Invalid dialogue form")
                if s2[0] not in names:
                    print(s[0])
                    raise ValueError("A character that has dialogue is not in character list")
                if s2[0] not in characters_in_scene:
                    print(s2[0],"in",s[0])
                    print(characters_in_scene)
                    raise ValueError("A character that is not in scene has dialogue")
                if s2[2] not in emotion_slot:
                    print(s2[2])
                    print(s2)
                    raise ValueError("Invalid value in emotion slot")
            case 3:#c
                if s[0]!='change':
                    raise ValueError("First element of a scene change action is not 'change'")
                s2=s[1].split(',')
                characters_in_scene = []
                for c in s2:
                    if c not in names:
                        print(c)
                        raise ValueError("A character in scene but not in character list")
                    characters_in_scene.append(c)
                if len(characters_in_scene)>4:
                    print(characters_in_scene)
                    print("Number of characters:",len(characters_in_scene))
                    raise ValueError("Too much characters in a scene")
            case 4:#t
                if s[0] not in throwables:
                    print(s[0])
                    raise ValueError("Invalid throwable")
                if s[1] not in throw_speeds:
                    print(s[1])
                    raise ValueError("Invalid throw speed")
                if s[2] not in names:
                    print(s[2])
                    raise ValueError("A character throwing a throwable is not in character list")
                if s[3] not in names:
                    print(s[3])
                    raise ValueError("A character throwing a throwable is not in character list")
                if s[2] not in characters_in_scene:
                    print(s[2])
                    raise ValueError("A character that is not in scene is throwing a throwable")
                if s[3] not in characters_in_scene:
                    print(s[3])
                    raise ValueError("A character that is not in scene is throwing a throwable")
            case _:
                print(s)
                raise ValueError("Invalid sequence element")
    print("Script passes the checks.")

def check_file_script(replace_GPT_aposthrophe:bool=True):
    with open("script.txt", 'r') as f:
        script = f.read()
    if replace_GPT_aposthrophe:
        with open("script.txt", 'w') as f:
            f.write(script.replace("â€™","'"))
    check_script(script)

check_file_script()