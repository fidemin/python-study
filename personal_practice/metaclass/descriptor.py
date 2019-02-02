

class Descriptor(object):
    def __get__(self, instance, cls):
        return "attr2 from descriptor"

    def __set__(self, istance, value):
        pass


class NotDescriptor(object):
    def __get__(self, instance, cls):
        return "attr3 from not_descriptor"


class Class(object):
    attr1 = "attr1 from Class"
    attr2 = Descriptor()
    attr3 = NotDescriptor()


    def __init__(self):
        self.attr1 = "attr1 from __init__"
        self.attr2 = "attr2 from __init__"
        self.attr3 = "attr3 from __init__"


if __name__ == "__main__":
    c = Class()
    print(c.attr1)
    print(c.attr2)
    print(c.attr3)
