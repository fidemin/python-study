
import unittest

from logic_gate import *

class TestLoginGate(unittest.TestCase):
    def test_and_gate(self):
        and_gate = AndGate('A')
        and_gate.set(0, 0)
        self.assertEqual(0, and_gate.operate())
        and_gate.set(1, 0)
        self.assertEqual(0, and_gate.operate())
        and_gate.set(1, 1)
        self.assertEqual(1, and_gate.operate())

    def test_or_gate(self):
        or_gate = OrGate('A')
        or_gate.set(0, 0)
        self.assertEqual(0, or_gate.operate())
        or_gate.set(1, 0)
        self.assertEqual(1, or_gate.operate())
        or_gate.set(0, 1)
        self.assertEqual(1, or_gate.operate())
        or_gate.set(1, 1)
        self.assertEqual(1, or_gate.operate())

    def test_not_gate(self):
        not_gate = NotGate('A')
        not_gate.set(0)
        self.assertEqual(1, not_gate.operate())
        not_gate.set(1)
        self.assertEqual(0, not_gate.operate())


    def test_complex_gates(self):
        gate1 = AndGate('1')
        gate1.set(1, 0)
        gate2 = AndGate('2')
        gate2.set(1, 1)
        gate3 = OrGate('3')
        gate4 = NotGate('4')
        gate3.set_next(gate1)
        gate3.set_next(gate2)
        gate4.set_next(gate3)
        self.assertEqual(0, gate4.operate())
        gate1.set(0, 1)
        gate2.set(1, 0)
        self.assertEqual(1, gate4.operate())


class TestConnector(unittest.TestCase):
    def test_connector(self):
        gate1 = AndGate('1')
        gate1.set(1, 0)
        gate2 = AndGate('2')
        gate2.set(1, 1)
        gate3 = OrGate('3')
        gate4 = NotGate('4')
        Connector.connect(gate1, gate3)
        Connector.connect(gate2, gate3)
        Connector.connect(gate3, gate4) 
        self.assertEqual(0, gate4.operate())
