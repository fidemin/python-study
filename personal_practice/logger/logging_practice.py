import logging


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, prefix, logger):
        super(LoggerAdapter, self).__init__(logger, {})
        self._prefix = prefix

    def process(self, msg, kwargs):
        return f"[{self._prefix}] - {msg}", kwargs


if __name__ == "__main__":
    # this is the root logger
    logging.error("This is an error message")
    logging.info("This is an info message")

    # this is a custom logger
    base_logger = logging.getLogger("my")

    base_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    base_logger.addHandler(stream_handler)

    file_handler = logging.FileHandler("my.log")
    file_handler.setFormatter(formatter)
    base_logger.addHandler(file_handler)

    base_logger.propagate = False

    mylogger = LoggerAdapter("MIN", base_logger)

    mylogger.info("server started")
    mylogger.error("server crashed")
