def list2string(list):
    s = ""
    for l in list:
        if l == 127:
            break
        if chr(l) == ',':
            print("COMMA")
        s += chr(l)
    return s
