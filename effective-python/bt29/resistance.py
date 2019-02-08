
class Resistor(object):
    def __init__(self, ohms):
        print('init ohms')
        self.ohms = ohms
        print('init next') 
        self.voltage = 0
        self.current = 0


class BoundedResistance(Resistor):
    def __init__(self, ohms): 
        super().__init__(ohms)


    @property
    def ohms(self):
        return self._ohms


    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        print('ohms.setter!', ohms)
        self._ohms = ohms


class FixedResistance(Resistor):
    def __init__(self, ohms): 
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


if __name__ == "__main__":
    r3 = BoundedResistance(1e3)
    print(r3.ohms)
    r4 = FixedResistance(1e4)
    r4.ohms = 2e3


