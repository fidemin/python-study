from decimal import Decimal
import decimal

if __name__ == "__main__":
    rate = 1.45
    seconds = 3*60 + 42
    cost = rate * seconds / 60
    print(cost)
    print(round(cost, 2)) # 반올림


    rate = 0.05
    seconds = 5
    cost = rate * seconds / 60
    print(cost)
    print(round(cost, 2))

    rate = Decimal('0.05')
    seconds = Decimal('5')
    cost = rate * seconds / Decimal('60')
    print(cost)
    rounded = cost.quantize(Decimal('0.01'), rounding=decimal.ROUND_UP)
    print(rounded)
