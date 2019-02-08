
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)


class MyClass(object, metaclass=Meta):
    stuff = 123

    def foo(self):
        pass


if __name__ == "__main__":
    pass
