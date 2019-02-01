#!/usr/bin/env python3

import logging
import time
from concurrent.futures import ThreadPoolExecutor

import grpc

from api.v1.services import customers as customers_svc

def main(args):
    """
    Service Main

    :param args: parsed cli flags
    """
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
    logging.basicConfig()
    main([])

