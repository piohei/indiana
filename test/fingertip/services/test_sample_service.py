# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, MagicMock

from test.factory import *

from exception import SampleException
from fingertip.services import *


class TestSampleService(unittest.TestCase):

    def setUp(self):
        self.sample_stamp_dao = Mock()
        self.ap_data_dao = Mock()
        self.under_test = SampleService(self.ap_data_dao, self.sample_stamp_dao)

    def test_set_sample_stamp_none_previously(self):
        self.assertIsNone(self.under_test.current_sample_stamp)
        new_stamp = Mock()
        new_stamp.is_same = Mock(return_value=False)
        self.under_test.set_sample_stamp(new_stamp)
        self.assertIs(new_stamp, self.under_test.current_sample_stamp)
        new_stamp.is_same.assert_called_once_with(None)

    def test_end_fingertip_if_present_and_not_ended(self):
        old_stamp = Mock()
        self.under_test.current_sample_stamp = old_stamp

        self.under_test.end_sample()

        old_stamp.end.assert_called_once_with()
        self.sample_stamp_dao.save.assert_called_once_with(old_stamp)
        self.assertIsNone(self.under_test.current_sample_stamp)

    def test_set_sample_stamp_old_different_present(self):
        old_stamp = Mock()
        self.under_test.current_sample_stamp = old_stamp
        new_stamp = Mock()
        new_stamp.is_same = Mock(return_value=False)

        self.under_test.set_sample_stamp(new_stamp)

        self.assertIs(new_stamp, self.under_test.current_sample_stamp)
        new_stamp.is_same.assert_called_once_with(old_stamp)
        old_stamp.end.assert_called_once_with()
        self.sample_stamp_dao.save.assert_called_once_with(old_stamp)

    def test_set_sample_stamp_old_same_present(self):
        old_stamp = Mock()
        self.under_test.current_sample_stamp = old_stamp
        new_stamp = Mock()
        new_stamp.is_same = Mock(return_value=True)

        self.assertRaises(SampleException, self.under_test.set_sample_stamp, new_stamp)
        self.assertIs(old_stamp, self.under_test.current_sample_stamp)
        old_stamp.end.assert_not_called()

    def test_end_sample_if_none(self):
        self.assertIsNone(self.under_test.current_sample_stamp)

        self.assertRaises(SampleException, self.under_test.end_sample)
        self.assertIsNone(self.under_test.current_sample_stamp)

    def test_end_sample_with_exception(self):
        old_stamp = Mock()
        old_stamp.end = Mock(side_effect=SampleException("message"))
        self.under_test.current_sample_stamp = old_stamp

        self.assertRaises(SampleException, self.under_test.end_sample)
        self.assertIsNone(self.under_test.current_sample_stamp)
        old_stamp.end.assert_called_once_with()
        self.sample_stamp_dao.save.assert_not_called()

    def test_end_if_outdated_no_stamp(self):
        self.assertIsNone(self.under_test.current_sample_stamp)
        # passes silently
        self.under_test.end_if_outdated()

    def test_end_if_outdated_not_outdated(self):
        old_stamp = Mock()
        old_stamp.is_outdated = Mock(return_value=False)
        self.under_test.current_sample_stamp = old_stamp

        self.under_test.end_if_outdated()

        old_stamp.is_outdated.assert_called_once_with()
        self.assertIs(old_stamp, self.under_test.current_sample_stamp)
        old_stamp.end.assert_not_called()

    def test_end_if_outdated_when_outdated(self):
        old_stamp = Mock()
        old_stamp.is_outdated = Mock(return_value=True)
        self.under_test.current_sample_stamp = old_stamp

        self.under_test.end_if_outdated()

        old_stamp.is_outdated.assert_called_once_with()
        self.assertIsNone(self.under_test.current_sample_stamp)
        old_stamp.end.assert_called_once_with()
        self.sample_stamp_dao.save.assert_called_once_with(old_stamp)

    def test_save_ap_data_stamp_present_and_valid(self):
        old_stamp = Mock()
        self.under_test.current_sample_stamp = old_stamp

        ap_data = Mock()

        self.under_test.save_ap_data_for_sample(ap_data)

        self.ap_data_dao.save.assert_called_once_with(ap_data)

    def test_get_status_when_none(self):
        self.assertIsNone(self.under_test.current_sample_stamp)
        self.assertEqual("no fingertip", self.under_test.get_status())
        self.ap_data_dao.count.assert_not_called()

    def test_get_status_when_present(self):
        old_stamp = Mock()
        old_stamp.start_time = Time(1)
        self.under_test.current_sample_stamp = old_stamp
        self.ap_data_dao.count = Mock(return_value=10)
        self.assertEqual("{}: collected {}".format(old_stamp, 10), self.under_test.get_status())
        self.ap_data_dao.count.assert_called_once_with({
            'created_at': {
                '$gt': 1
            }
        })


if __name__ == '__main__':
    unittest.main()
