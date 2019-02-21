import time

from collections import deque

def bind(instance, name, func):
    setattr(instance, 'execute', func.__get__(instance, instance.__class__))


class ActiveObjectEngine(object):
    def __init__(self):
        self._commands = deque([])

    def add_command(self, c):
        self._commands.append(c)

    def run(self):
        while len(self._commands) is not 0:
            c = self._commands.popleft()
            c.execute()


class Command(object):
    def execute(self):
        pass


class SleepCommand(Command):
    def __init__(self, sleeptime, engine, wakeup_command):
        self._engine = engine
        self._wakeup_command = wakeup_command
        self._started = False
        self._start_time = 0
        self._sleep_time = sleeptime

    def execute(self):
        if not self._started:
            self._started = True
            self._start_time = time.time() * 1000
            self._engine.add_command(self)
            return

        current = time.time() * 1000
        if self._sleep_time > (current - self._start_time):
            self._engine.add_command(self)
        else:
            self._engine.add_command(self._wakeup_command)


class DelayedTyper(Command):
    stop = False

    def __init__(self, engine, delay, char):
        self._delay = delay
        self._char = char
        self._engine = engine

    def execute(self):
        print(self._char, end='')
        if not self.stop:
            self._delay_and_repeat()

    def _delay_and_repeat(self):
        self._engine.add_command(SleepCommand(self._delay, self._engine, self))


if __name__ == "__main__":
    e = ActiveObjectEngine()

    def stop_to_true(self):
        DelayedTyper.stop = True

    e.add_command(DelayedTyper(e, 100, '1'))
    e.add_command(DelayedTyper(e, 300, '3'))
    e.add_command(DelayedTyper(e, 500, '5'))
    e.add_command(DelayedTyper(e, 700, '7'))

    stop_command = Command()
    bind(stop_command, 'execute', stop_to_true)

    e.add_command(SleepCommand(5000, e, stop_command))
    e.run()

