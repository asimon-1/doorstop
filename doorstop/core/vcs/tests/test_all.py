# SPDX-License-Identifier: LGPL-3.0-only

"""Integration tests for the doorstop.vcs package."""

import unittest

import gitignorant

from doorstop.core.vcs import load
from doorstop.core.vcs.tests import ROOT


class TestWorkingCopy(unittest.TestCase):
    """Integration tests for a working copy."""

    @classmethod
    def setUpClass(cls):
        cls.wc = load(ROOT)

    def test_ignores(self):
        """Verify the ignores file is parsed."""
        patterns = [str(p) for p in self.wc.ignores]
        for pattern in patterns:
            print(pattern)

        self.assertIn(
            str(gitignorant.Rule(negative=False, content="__pycache__")), patterns
        )
        self.assertIn(
            str(gitignorant.Rule(negative=False, content="/build/")), patterns
        )
