
from argparse import ArgumentParser

from auth import models
from auth.services import users as users_svc


def parse_args():
    """Parse cli flags"""
    parser = ArgumentParser()
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("-p", "--password")
    parser.add_argument(
        "-A", "--admin",
        dest="is_admin",
        action="store_true")
    parser.add_argument("-f", "--first-name")
    parser.add_argument("-l", "--last-name")

    return parser.parse_args()


def create_user(args):
    """
    Create user
    """
    user = users_svc.create_user(args.__dict__)
    print("Created user:")
    print(user)


def __main__():
    args = parse_args()
    create_user(args)

