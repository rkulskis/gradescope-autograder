#!/usr/bin/env python3

import urllib.request

HARNESS_URL = 'https://s3-us-west-2.amazonaws.com/gradescope-static-assets/autograder/python3/harness.py'


def version(harness_string):
    """ Returns the version from the second line, which looks like
    # Version: 0.10.0
    """
    lines = harness_string.split("\n")
    version_string = lines[1][11:]
    return [int(x) for x in version_string.split(".")]


def is_newer_version(new, old):
    for digit in range(0, 3):
        # If new digit matches old, keep checking next digit
        if new[digit] == old[digit]:
            continue
        # If new digit is greater, the version is higher, else, it's lower
        return new[digit] > old[digit]
    # This case is only reached when the digits are exactly the same
    return False


def update_harness():
    new_harness = urllib.request.urlopen(HARNESS_URL).read().decode("utf-8")
    with open("/autograder/harness.py", "r") as f:
        old_harness = f.read()

    new_version = version(new_harness)
    old_version = version(old_harness)

    if is_newer_version(new_version, old_version):
        with open("/autograder/harness.py", "w") as f:
            f.write(new_harness)

if __name__ == "__main__":
    update_harness()
