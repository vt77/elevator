


handlers = []

def fireStatusChange(name,event):
    for h in handlers:
        h(name,event)

def statuschange(func):
    handlers.append(func)
