import time
import unittest

from command import bind
from command import ActiveObjectEngine, Command, SleepCommand

executed = False


class TestSleepCommand(unittest.TestCase):
    def test_sleep(self):
        comm_wakeup = Command()

        def binding_func(self):
            global executed
            executed = True


        bind(comm_wakeup, 'execute', binding_func)

        e = ActiveObjectEngine()
        c = SleepCommand(1000, e, comm_wakeup)
        e.add_command(c)
        start = time.time() * 1000
        e.run()
        end = time.time() * 1000
        sleeptime = end - start

        self.assertTrue(sleeptime > 1000)
        self.assertTrue(sleeptime < 1200)
        self.assertTrue(executed)


if __name__ == "__main__":
    unittest.main()
