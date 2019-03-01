
class Name(object):
    def __get__(self, instance, cls):
        return instance


class Example(object):
    name = Name()



# property decorator를 쓰는게 더편한다.
class C(object):
    def getx(self): return self.__x
    def setx(self, value): self.__x = value
    def delx(self): del self.__x
    def what(self): pass
    x = property(getx, setx, delx, "I'm the 'x' property.")


def example_func(self):
    return 'what?'


if __name__ == "__main__":
    e = Example()
    descriptor = Name()
    print(descriptor.__get__(e, e.__class__))
    print(e.name)

    c1 = C()
    c1.setx(10)
    c2 = C()
    c2.setx(20)

    print(c1.x)
    print(c2.x)

    #print(example_func.__get__(c1, type(c1)))

    # 동적으로 메소드 할당
    setattr(c1, 'what', example_func.__get__(c1, type(c1)))
    print(c1.what)
    print(c1.what())
