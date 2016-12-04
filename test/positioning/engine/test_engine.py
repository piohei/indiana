# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from positioning.engine import Engine, EngineException
from positioning.chains.base import Base


class PassArgs(Base):
    def calculate(self, **kwargs):
        return kwargs


class Alpha(Base):
    def links(self):
        return [
            PassArgs,
            PassArgs
        ]

Engine.CHAINS["alpha"] = Alpha


class TestEngine(unittest.TestCase):
    def test_engine_creating_with_wrong_link(self):
        with self.assertRaises(EngineException):
            Engine(chain='wrong_name')

    def test_engine_creating_with_right_link(self):
        Engine(chain='alpha')
        self.assertTrue(True)

    def test_engine_uses_alpha_to_calculate(self):
        en = Engine(chain='alpha')
        self.assertEqual(en.calculate(fingertips=(1, 2, 3))["fingertips"], (1, 2, 3))
        self.assertEqual(en.calculate(fingertips=(1, 2, 3, 4, 5))["fingertips"], (1, 2, 3, 4, 5))
        self.assertEqual(en.calculate(fingertips=(1, 2, "test", 2.5))["fingertips"], (1, 2, "test", 2.5))


if __name__ == '__main__':
    unittest.main()
