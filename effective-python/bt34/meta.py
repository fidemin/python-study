import json

_registered_class = {}

class SerializableMeta(type):
    _registered_class = {}
    def __new__(meta, name, bases, class_dict):
        #print('meta:', meta, '\nname:', name, '\nbases:', bases, '\nclass_dict:', class_dict)
        cls = type.__new__(meta, name, bases, class_dict)
        _registered_class[cls.__name__] = cls
        return cls


class Serializable(object, metaclass=SerializableMeta):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })

    def __repr__(self):
        values = ", ".join(map(str, self.args))
        return '%s(%s)' % (self.__class__.__name__, values)


def deserialize(data):
    params = json.loads(data)
    cls = _registered_class[params['class']]
    return cls(*params['args'])


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y


if __name__ == "__main__":
    p2 =  Point2D(3, 5)
    print('before:', p2)
    serialized = p2.serialize()
    print('Serialized:', serialized)
    deserialized = deserialize(serialized)
    print('after:', deserialized)
