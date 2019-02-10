

import logging

from db import engine


LOG_FORMAT = "%(asctime)s [%(levelname)s] %(module)s: %(message)s"


def application_init():
    """
    Bootstrap server application
    """
    # Setup logging
    logging.basicConfig(format=LOG_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Make database connection
    engine.connect("sqlite:///var/db.sqlite3")

