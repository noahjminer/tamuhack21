def list2string(list):
    s = ""
    for l in list:
        if l == 127:
            break
        s += chr(l)
    return s
