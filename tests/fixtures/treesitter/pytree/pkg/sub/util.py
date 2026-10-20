import re


def helper(pattern, text="", *rest):
    """Find pattern."""
    return re.search(pattern, text)


def _private_helper():
    pass


class Tool:
    def run(self):
        return helper("a")

    def run_again(self):
        return helper("b")
