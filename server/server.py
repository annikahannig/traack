#!/usr/bin/env python3

import logging
import time
from concurrent.futures import ThreadPoolExecutor

import grpc

from api.v1.services import customers as customers_svc
from db import engine


LOG_FORMAT = "%(asctime)s [%(levelname)s] %(module)s: %(message)s"


def init():
    """
    Bootstrap server application
    """
    # Setup logging
    logging.basicConfig(format=LOG_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Make database connection
    engine.connect("sqlite:///var/db.sqlite3")


def main(args):
    """
    Service Main

    :param args: parsed cli flags
    """
    init()

    # Create GRPC server
    server = grpc.server(ThreadPoolExecutor(max_workers=10))

    # Register services
    customers_svc.register(server)

    # Start listen and serve
    server.add_insecure_port('[::]:2344')
    server.start()

    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    main([])

