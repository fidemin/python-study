
class Parent(object):
    def __init__(self, name):
        self._who()
        self.name = name

    def _who(self):
        print("this is Parent")


class Child(Parent):
    def __init__(self, name):
        # super에서 실행되는 init이지만 _who 메서드는
        # child 것을 사용한다.
        super().__init__(name)

    def _who(self):
        print("this is Child")


if __name__ == "__main__":
    p = Parent("Yunhong")
    c = Child("Junghyun")
