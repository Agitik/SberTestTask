import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="ServerLog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    filemode="w",
)

logger = logging.getLogger(__name__)
