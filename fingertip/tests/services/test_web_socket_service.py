# -*- coding: utf-8 -*-
from tornado.websocket import WebSocketClosedError

from fingertip.services import WebSocketService

import unittest
from unittest.mock import Mock

MESSAGE = "message"


class TestWebSocketService(unittest.TestCase):
    def assert_closed_with_message(self, sock, message):
        sock.write_message.assert_called_once_with(message)
        sock.close.assert_called_once_with()

    def assert_list(self, expected):
        self.assertListEqual(expected, self.under_test.list)

    def setUp(self):
        self.under_test = WebSocketService()
        self.sock1 = Mock()
        self.sock2 = Mock()

    def add_two_sockets(self):
        self.under_test.add_socket(self.sock1)
        self.under_test.add_socket(self.sock2)

    def test_add_socket(self):
        self.add_two_sockets()

        self.assert_list([self.sock1, self.sock2])

    def test_remove_socket(self):
        self.add_two_sockets()

        self.under_test.remove_socket(self.sock1)
        self.assert_list([self.sock2])
        self.assert_closed_with_message(self.sock1, "")

        self.under_test.remove_socket(self.sock2, MESSAGE)
        self.assert_list([])
        self.assert_closed_with_message(self.sock2, MESSAGE)

    def test_remove_closed_socket_passes(self):
        self.add_two_sockets()
        self.sock2.write_message = Mock(side_effect=WebSocketClosedError())

        self.under_test.remove_socket(self.sock2, MESSAGE)

        self.assert_list([self.sock1])
        self.assert_closed_with_message(self.sock2, MESSAGE)

    def test_close_current_sockets(self):
        self.add_two_sockets()

        self.under_test.close_current_sockets()

        self.assert_list([])
        self.assert_closed_with_message(self.sock1, "closed")
        self.assert_closed_with_message(self.sock2, "closed")

    def test_broadcast(self):
        self.add_two_sockets()
        self.sock2.write_message = Mock(side_effect=WebSocketClosedError())

        self.under_test.broadcast(MESSAGE)
        self.sock1.write_message.assert_called_once_with(MESSAGE)
        self.sock2.write_message.assert_called_once_with(MESSAGE)



if __name__ == '__main__':
    unittest.main()
