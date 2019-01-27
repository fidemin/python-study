
class LogicGate(object):
    def __init__(self, label):
        self._label = label

    def operate(self):
        raise NotImplementedError("operate method should be implemented")


class BinaryGate(LogicGate):
    def __init__(self, label):
        super(BinaryGate, self).__init__(label)
        self._a = None
        self._b = None

    def set(self, a, b):
        self._a = a
        self._b = b

    def set_next(self, a):
        if self._a == None:
            self._a = a
        elif self._b == None:
            self._b = a
        else:
            raise Exception("not available conneciton spot")


    def _get_a(self):
        if self._a is not None:
            if hasattr(self._a, 'operate'):
                return self._a.operate()
            else:
                return self._a 
        else:
            raise Exception("two binary values or logic gate should be set")

    def _get_b(self):
        if self._b is not None:
            if hasattr(self._b, 'operate'):
                return self._b.operate()
            else:
                return self._b
        else:
            raise Exception("two binary values or logic gate should be set")


class UnaryGate(LogicGate):
    def __init__(self, label):
        super(UnaryGate, self).__init__(label)
        self._a = None

    def set(self, a):
        self._a = a

    def set_next(self, a):
        if self._a == None:
            self._a = a
        else:
            raise Exception("not available conneciton spot")


class AndGate(BinaryGate):
    def operate(self):
        a = self._get_a()
        b = self._get_b()
        return a & b


class OrGate(BinaryGate):
    def operate(self):
        a = self._get_a()
        b = self._get_b()
        return a | b


class NotGate(UnaryGate):
    def operate(self):
        if self._a is None:
            raise Exception("one binary value should be set for NotGate")

        if hasattr(self._a, 'operate'):
            a = self._a.operate()
        else:
            a = self._a

        if a == 0:
            return 1

        elif a == 1:
            return 0


class Connector(object):
    @staticmethod
    def connect(fr, to):
        try:
            to.set_next(fr)
        except Exception as e:
            raise





