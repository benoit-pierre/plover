
import unittest

from plover import system
from plover.registry import registry
from plover.config import DEFAULT_SYSTEM


class PloverTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        registry.update()
        system.setup(DEFAULT_SYSTEM)

