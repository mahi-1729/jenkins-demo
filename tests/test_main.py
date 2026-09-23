import sys
import os

sys.path.insert(0, os.path.abspath("app"))

from main import add, get_message


def test_add():
    assert add(2, 3) == 5


def test_message():
    assert get_message() == "Hello from Jenkins CI!"
