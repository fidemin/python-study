
from models import Model, Field

class Customer(Model):
    first_name = Field()
    last_name = Field()


if __name__ == "__main__":
    c = Customer()
    print('Before: ', repr(c.first_name), c.__dict__)
    c.first_name = "Yunhong Min"
    print('After: ', repr(c.first_name), c.__dict__)
