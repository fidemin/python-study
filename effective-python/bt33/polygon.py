
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # DO NOT Validate abstract Polygon class
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygon need 3+ sides')

        return type.__new__(meta, name, bases, class_dict)


class Polygon(object, metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


if __name__ == "__main__":
    print('Before class')
    class Line(Polygon):
        print('Before sides')
        sides = 1
        print('After sides')

    print('After class')
