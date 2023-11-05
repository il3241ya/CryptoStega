from termcolor import colored


def rprint(out_message):
    """
    Print colored messages in red.

    Args:
        out_message: Messages to print.
    """
    print(colored(out_message, 'red'))


def bprint(out_message):
    """
    Print colored messages in blue.

    Args:
        out_message: Messages to print.
    """
    print(colored(out_message, 'blue'))


def gprint(out_message):
    """
    Print colored messages in green.

    Args:
        out_message: Messages to print.
    """
    print(colored(out_message, 'green'))
