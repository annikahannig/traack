#!/usr/bin/env python3
"""
Launch a python shell

Try to launch ipthon or bpython. Fall back to the
standard python interpreter.
"""

def start_ipython(user_ns={}):
    """Start the ipython shell"""
    from IPython import start_ipython
    start_ipython(argv=[], user_ns=user_ns)


def start_bpython(locals_={}):
    """Start the bpython shell"""
    from bpython import embed
    embed(locals_=locals_)


def start_fallback(local={}):
    """Start the fallback interpreter"""
    from code import interact
    interact(local=local)


def start_shell(local={}):
    """
    Start a python shell
    """
    shells = [start_ipython, start_bpython, start_fallback]
    for shell in shells:
        try:
            shell(local)
        except ImportError:
            pass # try next
        else:
            return


def __main__():
    """
    Start the API console
    """
    start_shell()

