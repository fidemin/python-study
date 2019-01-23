from datetime import datetime
from time import sleep

def log(msg, when=datetime.now()):
    print("%s: %s" % (when, msg))

def log_right(msg, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print
        when: datetime of when the message occured.
            Defaults to the present time.
    """
    when = datetime.now() if when is None else when
    print ("%s: %s" % (when, msg))


if __name__ == "__main__":
    log_right("hi")
    sleep(0.1)
    log_right("hi")
