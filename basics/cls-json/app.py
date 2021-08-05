import json


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class JsonCls(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


jcls = JsonCls(100, 'Ocean')

print(json.dumps(jcls.__dict__))
print(JsonEncoder().encode(jcls))
