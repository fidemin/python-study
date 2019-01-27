
class LogicGate(object):
    def __init__(self, label):
        self._label = label

    def operate(self):
        raise NotImplementedError("operate method should be implemented")


    def set_next(self, a):
        for i, value in enumerate(self._inputs):
            if value is None:
                self._inputs[i] = a
                return

        self._raise_not_available_spot()


    def _raise_not_available_spot(self):
        raise Exception("not available conneciton spot for logic gate '%s'" % (self._label))

    def _raise_not_enough_inputs(self):
        raise Exception(
            "%d binary values or logic gate should be set for logic gate '%s'" % (self.num_of_input, self._label)
        )

class BinaryGate(LogicGate):
    num_of_input = 2

    def __init__(self, label):
        super(BinaryGate, self).__init__(label)
        self._inputs = [None, None]


    def set(self, a, b):
        self._inputs = [a, b]

    def _get_inputs(self):
        result = []
        for value in self._inputs:
            if value is None:
                self._raise_not_enough_inputs()

            if hasattr(value, 'operate'):
                result.append(value.operate())
            else:
                result.append(value)

        return tuple(result)


class UnaryGate(LogicGate):
    num_of_input = 1
    def __init__(self, label):
        super(UnaryGate, self).__init__(label)
        self._inputs = [None]

    def set(self, a):
        self._inputs = [a]


class AndGate(BinaryGate):
    def operate(self):
        a, b = self._get_inputs()
        return a & b


class OrGate(BinaryGate):
    def operate(self):
        a, b = self._get_inputs()
        return a | b


class NotGate(UnaryGate):
    def operate(self):
        value = self._inputs[0]
        if value is None:
            self._raise_not_enough_inputs()

        if hasattr(value, 'operate'):
            a = value.operate()
        else:
            a = value

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
