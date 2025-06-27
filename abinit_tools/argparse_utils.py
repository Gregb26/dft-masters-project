# abinit_tools/argparse_utils.py

import argparse

def parse_args(description=None, positional_args=None, optional_args=None):
    """
    General purpose CLI argument parser
    Inputs:
        description (str): Description of the script's purpose
        positional_args (list of tuples): List of positional arguments (name, help_text).
        optional_args (list of dicts): Each dict defines optional arguments argument, passed to "add_arguments(**kwargs)".
    Returns:
        argparse.Namespace: Parsed arguments.
    """

    parser = argparse.ArgumentParser(description=description)

    # positional arguments
    if positional_args:
        for name, help_text in positional_args:
            parser.add_argument(name, help=help_text)

    # optional arguments
    if optional_args:
        for opt in optional_args:
            for flag, kwargs in opt.items():
                parser.add_argument(flag, **kwargs)

    return parser.parse_args()
