
def value_changer(start_value):
    while True:
        start_value = yield start_value

if __name__ == "__main__":
    vc = value_changer("1")
    print(next(vc))
    print(vc.send("2"))
