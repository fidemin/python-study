

class Descriptor(object):
    def __get__(self, instance, cls):
        return "attr2 from descriptor"

    def __set__(self, istance, value):
        pass


class NoDescriptor(object):
    def __get__(self, instance, cls):
        return "attr3 from no_descriptor"


class Class(object):
    attr1 = "attr1 from Class"
    attr2 = Descriptor()
    attr3 = NoDescriptor()

    def __init__(self):
        self.attr1 = "attr1 from __init__"
        self.attr2 = "attr2 from __init__"
        self.attr3 = "attr3 from __init__"
        #self.attr4 = "attr4 from __init__"

    def __getattribute__(self, attr):
        print('-- get attribute called --')
        return super().__getattribute__(attr)

    def __getattr__(self, attr):
        return '%s from __getattr__' % attr


if __name__ == "__main__":
    c = Class()
    print(c.attr1)
    print(c.attr2)
    print(c.attr3)
    print(c.attr4)
