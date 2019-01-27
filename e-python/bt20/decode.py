import json

def decode_wrong(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default

def decode(data, default=None):
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            return {}
        return default


foo = decode('bad data')
foo['stuff'] = 10
bar = decode('also bad')
bar['good'] = 5

print("Foo:", foo)
print("Bar:", bar)
