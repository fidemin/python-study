

class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value


class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        return super().__getattribute__(name)

    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value


class LoggingSavingDB(ValidatingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__ (%s, %r)' % (name, value))
        super().__setattr__(name, value)


class DictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]


if __name__ == "__main__":
    data = LoggingSavingDB()
    print('before:', data.__dict__)
    print('foo:   ', data.foo)
    print('after:', data.__dict__)

    data = DictionaryDB({'foo':'bar'})
    print(data.foo)
