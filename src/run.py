import logging
from logging.handlers import RotatingFileHandler


def setup_logging(path, level='INFO'):
    handlers = [logging.StreamHandler()]
    file_path = path
    if file_path:
        file_handler = RotatingFileHandler(filename=file_path,
                                           maxBytes=10 * 10 * 1024 * 1024,
                                           backupCount=5)
        handlers.append(file_handler)
    logging.basicConfig(
        format='[{asctime}][{levelname}] - {name}: {message}',
        style='{',
        level=logging.getLevelName(level),
        handlers=handlers,
    )


class CNDProject:
    def __init__(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()


if __name__ == '__main__':
    setup_logging(**args)
    logger = logging.getLogger(__name__)
    project = None
    try:
        project = CNDProject(**args)
        project.start()
    except Exception as e:
        logger.exception(e)
    finally:
        if project is not None:
            project.stop()
