#!/usr/bin/env python3

import importlib
import glob
import sys

from bootstrap import application_init


def _module_from_path(path):
    """Make module from path"""
    path = path.replace(".py", "").replace(".", "").replace("/", ".")[1:]
    tokens = path.split('.')

    return (tokens[-1], path)


def import_scripts():
    """
    Import all scripts in script directory
    """
    script_path = "./management/scripts/"
    scripts = [_module_from_path(s) for s in glob.glob(script_path + "*.py")]

    script_modules = {name: importlib.import_module(module)
                      for name, module in scripts
                      if name != "__init__"}

    return script_modules


def print_usage():
    """Show short help text"""
    print("Usage:")
    print("   ./manage.py <script_name> <args>")


def print_available_scripts(scripts):
    """Show scripts available"""
    print("Scripts:")
    for script in scripts.keys():
        print(" - {}".format(script))

def manage_cli():
    # Load script
    scripts = import_scripts()

    # Prepare argv
    if len(sys.argv) == 1:
        print_usage()
        print_available_scripts(scripts)
        return

    # Strip script from argv
    script_name = sys.argv[1]
    sys.argv = sys.argv[:1] + sys.argv[2:]

    # Setup application
    application_init()

    # Run script
    scripts[script_name].__main__()


if __name__ == "__main__":
    manage_cli()

