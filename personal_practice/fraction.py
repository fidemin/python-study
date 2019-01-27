
def gdc(m, n):
    while m % n != 0:
        old_m = m
        old_n = n

        m = old_n
        n = old_m % old_n

    return n


class Fraction(object):
    def __init__(self, top, bottom):
        self._num = top 
        self._den = bottom

    @property
    def numerator(self):
        return self._num

    @property
    def denominator(self):
        return self._den

    def __add__(self, frac):
        denominator = self.denominator * frac.denominator
        numerator = self.numerator * frac.denominator + self.denominator * frac.numerator

        common = gdc(abs(numerator), denominator)

        return Fraction(numerator // common, denominator // common)

    def __sub__(self, frac):
        denominator = self.denominator * frac.denominator
        numerator = self.numerator * frac.denominator - self.denominator * frac.numerator

        common = gdc(abs(numerator), denominator)

        return Fraction(numerator // common, denominator // common)

    def __str__(self):
        return "%d/%d" % (self._num, self._den)

    def __eq__(self, frac):
        first = self.denominator * frac.numerator 
        second = self.numerator * frac.denominator
        return first == second



if __name__ == "__main__":
    frac1 = Fraction(1, 4)
    frac2 = Fraction(1, 2)
    frac3 = frac1 + frac2
    frac4 = frac1 - frac2

    assert(frac3 == Fraction(6, 8))
    assert(frac4 == Fraction(-1, 4))
