# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

from yaml2ical import index


class IndexTestCase(unittest.TestCase):

    def setUp(self):
        # Make 23 entries as 23 is a prime number
        self.meetings = [x for x in range(1, 24)]

    def test_batch_meetings_3_cols(self):
        # NOTE(jlvillal): Please format the expected values to easily see the
        # columns and rows
        tests = (
            # 1 row
            (1, [1]),
            (2, [1, 2]),
            (3, [1, 2, 3]),
            # 2 rows
            (4, [1, 3, 4,
                 2]),
            (5, [1, 3, 5,
                 2, 4]),
            # 3 rows
            (7, [1, 4, 6,
                 2, 5, 7,
                 3]),
            (9, [1, 4, 7,
                 2, 5, 8,
                 3, 6, 9]),
            # 4 rows
            (11, [1, 5, 9,
                  2, 6, 10,
                  3, 7, 11,
                  4, 8]),
            # 8 rows
            (23, [1, 9, 17,
                  2, 10, 18,
                  3, 11, 19,
                  4, 12, 20,
                  5, 13, 21,
                  6, 14, 22,
                  7, 15, 23,
                  8, 16]),
        )

        for test_length, expected in tests:
            self.assertEqual(
                expected, index.batch_meetings(self.meetings[:test_length], 3))

    def test_batch_meetings_4_cols(self):
        # NOTE(jlvillal): Please format the expected values to easily see the
        # columns and rows
        tests = (
            # Empty
            (0, []),
            # 1 row
            (1, [1]),
            (2, [1, 2]),
            (3, [1, 2, 3]),
            (4, [1, 2, 3, 4]),
            # 2 rows
            (5, [1, 3, 4, 5,
                 2]),
            (7, [1, 3, 5, 7,
                 2, 4, 6]),
            (8, [1, 3, 5, 7,
                 2, 4, 6, 8]),
            # 3 rows
            (9, [1, 4, 6, 8,
                 2, 5, 7, 9,
                 3]),
            (11, [1, 4, 7, 10,
                  2, 5, 8, 11,
                  3, 6, 9]),
            # 5 rows
            (23, [1, 7, 13, 19,
                  2, 8, 14, 20,
                  3, 9, 15, 21,
                  4, 10, 16, 22,
                  5, 11, 17, 23,
                  6, 12, 18]),
        )

        for test_length, expected in tests:
            self.assertEqual(
                expected, index.batch_meetings(self.meetings[:test_length], 4))

        # Make sure our docstring example is correct
        self.assertEqual(
            ['A', 'D', 'F', 'H',
             'B', 'E', 'G', 'I',
             'C'],
            index.batch_meetings(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                                 4))

    def test_batch_meetings_misc_cols(self):
        # Test various column values and inputs

        # NOTE(jlvillal): Please format the expected values to easily see the
        # columns and rows
        tests = (
            # Formatted as:
            # Number of items, columns, expected_result

            # Empty
            (0, 1, []),
            # 2 rows
            (8, 5, [1, 3, 5, 7, 8,
                    2, 4, 6]),
            (10, 6, [1, 3, 5, 7, 9, 10,
                     2, 4, 6, 8, ]),
            (7, 6, [1, 3, 4, 5, 6, 7,
                    2]),
        )

        for test_length, columns, expected in tests:
            self.assertEqual(
                expected,
                index.batch_meetings(self.meetings[:test_length], columns))

    def test_batch_meetings_zero_or_less(self):
        # Make sure we return the passed in value if columns less than or equal
        # to zero
        self.assertEqual([1, 2], index.batch_meetings([1, 2], 0))
        self.assertEqual([1, 2], index.batch_meetings([1, 2], -1))
        self.assertEqual([1, 2], index.batch_meetings([1, 2], -5551.5))

    def test_batch_meetings_sanity_check_not_triggered(self):
        # Make sure that an input containing None, False, 0, or "" doesn't
        # trigger the assert
        self.assertEqual([None, None], index.batch_meetings([None, None], 1))
        self.assertEqual(
            [False, False], index.batch_meetings([False, False], 1))
        self.assertEqual([0, 0], index.batch_meetings([0, 0], 4))
        self.assertEqual(["", ""], index.batch_meetings(["", ""], 1))
