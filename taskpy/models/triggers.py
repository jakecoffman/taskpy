import json

# name mapping to type and value
self = dict()

def get():
    global self
    return self

def save():
    global self
    open('triggers.json', 'w').write(json.dumps(self))

def load():
    global self
    try:
        self = json.loads(open('triggers.json').read())
    except:
        self = dict()
        save()

def add_trigger(name, type=None, value=None):
    global self
    self[name] = (type, value)
    save()
    
def delete_trigger(name):
    global self
    if name in self:
        del self[name]
        