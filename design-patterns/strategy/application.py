

class ApplicationRunner(object):
    def __init__(self, app):
        self._app = app

    def run(self):
        self._app.init()
        while not self._app.done():
            self._app.idle()

        self._app.cleanup()


class Application(object):
    def init(self):
        pass

    def idle(self):
        pass

    def cleanup(self):
        pass

    def done(self):
        return False


class FTOCApp(Application):
    def __init__(self):
        self._done = 0

    def idle(self):
        try:
            input_ = input("input fahr ['q' for quit]: ")
            if input_ == "q":
                self._done = True
                return

            fahr = float(input_)
            print(fahr)
        except ValueError as exc:
            print(exc)

    def done(self):
        return self._done


if __name__ == "__main__":
    app = FTOCApp()
    runner = ApplicationRunner(app)
    runner.run()
