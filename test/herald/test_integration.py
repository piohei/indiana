# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './../..')))

import unittest

from herald import *
from time import sleep

def message():
    return {
        'test': 'message',
        'value': 1,
    }

class TestPublisher(unittest.TestCase):

    def setUp(self):
        self.publisher = Publisher(key="test.1")
        self.subscriber1 = SynchronousSubscriber(key="test.1")
        self.subscriber2 = SynchronousSubscriber(key="test.2")
        self.subscriber = SynchronousSubscriber(key="test.*")

    def tearDown(self):
        self.publisher.destroy()
        self.subscriber1.destroy()
        self.subscriber2.destroy()
        self.subscriber.destroy()

    def test_one_receives(self):
        self.subscriber1.start()
        self.subscriber2.start()

        self.publisher.publish(message())

        m1 = self.subscriber1.get(timeout=5)
        m2 = self.subscriber2.get(timeout=5)

        self.subscriber1.stop()
        self.subscriber2.stop()

        self.assertEqual(m1, message())
        self.assertEqual(m2, None)

    def test_two_receive(self):
        self.subscriber1.start()
        self.subscriber2.start()
        self.subscriber.start()

        self.publisher.publish(message())

        m1 = self.subscriber1.get(timeout=5)
        m2 = self.subscriber2.get(timeout=5)
        m = self.subscriber.get(timeout=5)

        self.subscriber1.stop()
        self.subscriber2.stop()
        self.subscriber.stop()

        self.assertEqual(m1, message())
        self.assertEqual(m2, None)
        self.assertEqual(m, message())


if __name__ == '__main__':
    unittest.main()
