#!/usr/bin/env python3
# Copyright (c) 2018 enix223 <enix223@163.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import math
from enum import IntEnum
from functools import reduce

"""
1. Spiral Memory
You come across an experimental new kind of memory stored on an infinite two-dimensional grid.
Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then
counting up while spiraling outward. For example, the first few squares are allocated like this:

 .----------------.
 | 17 16 15 14 13 |
 | 18 5  4  3  12 |
 | 19 6  1  2  11 |
 | 20 7  8  9  10 |
 | 21 22 23 24 25 .
 .------------------>

While this is very space-efficient (no squares are skipped), requested data must be carried back to
square 1 (the location of the only access port for this memory system) by programs that can only
move up, down, left, or right. They always take the shortest path: the Manhattan Distance between
the location of the data and square 1.
For example:
Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all
the way to the access port?
Your Puzzle Input is: 2345678
Your Answer is: ?

Analyst
===========

elements in layer1 is 8,
elements in layer2 is 16,
elements in layer3 is 24...
elements in layern is n * 8

max number in layer1 is 9 = pow(3, 2),
max number in layer2 is 25 = pow(5, 2),
max number in layer3 is 49 = pow(7, 2),
max number is layern is pow(3 + 2 * (n - 1), 2)

The Manhattan Distance between X to 1 equal to n1 + n2
n1 = Which layer is number `X` is in
n2 = The shorted distance between the numbers on axis and `X`, n2 = min(x, y),

eg. When X = 30, layer = 3, numbers on axis for layer 3 are [28, 34, 40, 46],
and X is in range (28, 34), and X is more closer to 28, so n2 = 30 -28 = 2
So the distance between X to 1 is 3 + 2 = 5

                            ^
                            |      x = 34 - x1 = 4
                            [34]--------------------+
                            |                       |
                            |                       |
  X2                        [15]                    [X1] = 30
                            |                       |
                            |                       |
                            [4]                     | y = x1 - 28 = 2
                            |                       |
                            |                       |
----[40]----[19]----[6]---- [1] ----[2]----[11]----[28]---->
                            |
                            |
                            [8]
                            |
                            |
  X3                        [23]                     X4
                            |
                            |
                            [46]
                            |

Number set N1 in xAxis+ is [2, 11, 28, 53, ...],
N1 = {
    n[0] = 1, where l = 0
    n[l] = n[l - 1] + 8 * (l - 1) + 1, where l >= 1
}

Number set N2 in xAxis- is [6, 19, 40, 69, ...],
N2 = {
    n[0] = 1, where l = 0
    n[l] = n[l - 1] + 8 * (l - 1) + 5, l >= 1
}

Number set N3 in yAxis+ is [4, 15, 34, 61, ...],
N3 = {
    n[0] = 1, where l = 0
    n[l] = n[l - 1] + 8 * (l - 1) + 3, where l >= 1
}

Number set N4 in yAxis- is [8, 23, 46, 77, ...],
N4 = {
    n[0] = 1, where l = 0
    n[l] = n[l - 1] + 8 * (l - 1) + 7, l >= 1
}
"""


class QUADRANT(IntEnum):
    FIRST = 1,
    SECOND = 3,
    THIRD = 5,
    FOURTH = 7


def get_layer(n):
    """Get which layer is number `n` in. eg., 9 is in layer 1, 12 is in layer 2

    :param int n: The puzzle input number
    :return int: The layer# for input number `n`
    """
    n_root = math.sqrt(n)
    x = math.ceil(n_root)
    return math.ceil((x - 3) / 2 + 1)


def max_number_in_layer(layer):
    """Get the max number in layer
    """
    return int(math.pow(3 + 2 * (layer - 1), 2))


def get_number_on_axis_with_layer(layer, quadrant: QUADRANT):
    """Get the number on axis for `layer` and `quadrant`

    :param int layer: Which layer
    :param int quadrant: Which quadrant
    :return int: The number on the axis
    """
    if layer >= 1:
        num = reduce(lambda x, y: x + quadrant.value + (y - 1) * 8, range(1, layer + 1), 1)
        return num
    return 1


def get_shortest_distance_for_axis_intercept(n):
    """Get shorted distance between n and the 4 numbers on axis
    with same layer as n.

    :param int n: The puzzle input number
    :return int: The shortest distance
    """
    layer = get_layer(n)
    xaxis_1 = get_number_on_axis_with_layer(layer, QUADRANT.FIRST)
    yaxis_2 = get_number_on_axis_with_layer(layer, QUADRANT.SECOND)
    xaxis_3 = get_number_on_axis_with_layer(layer, QUADRANT.THIRD)
    yaxis_4 = get_number_on_axis_with_layer(layer, QUADRANT.FOURTH)
    max_num = max_number_in_layer(layer)

    if n >= xaxis_1 and n < yaxis_2:
        return min(n - xaxis_1, yaxis_2 - n)
    elif n >= yaxis_2 and n < xaxis_3:
        return min(n - yaxis_2, xaxis_3 - n)
    elif n >= xaxis_3 and n < yaxis_4:
        return min(n - xaxis_3, yaxis_4 - n)
    elif n >= yaxis_4 and n <= max_num:
        return n - yaxis_4
    else:
        return xaxis_1 - n


def calculate_distance(n):
    """The Manhattan Distance between `n` to 1

    :param int n: The puzzle input number
    :return int: The distance between `n` and `1`
    """
    n1 = get_layer(n)
    n2 = get_shortest_distance_for_axis_intercept(n)
    return n1 + n2


if __name__ == '__main__':
    if len(sys.argv) == 1:
        import unittest

        class TestSpiralMem(unittest.TestCase):
            def test_max_number_in_layer(self):
                self.assertEqual(max_number_in_layer(1), 9)
                self.assertEqual(max_number_in_layer(2), 25)
                self.assertEqual(max_number_in_layer(3), 49)
                self.assertEqual(max_number_in_layer(4), 81)

            def test_get_number_on_axis_with_layer(self):
                self.assertEqual(get_number_on_axis_with_layer(0, QUADRANT.FIRST), 1)
                self.assertEqual(get_number_on_axis_with_layer(1, QUADRANT.FIRST), 2)
                self.assertEqual(get_number_on_axis_with_layer(2, QUADRANT.FIRST), 11)
                self.assertEqual(get_number_on_axis_with_layer(4, QUADRANT.SECOND), 61)
                self.assertEqual(get_number_on_axis_with_layer(3, QUADRANT.THIRD), 40)
                self.assertEqual(get_number_on_axis_with_layer(4, QUADRANT.FOURTH), 77)

            def test_get_layer(self):
                self.assertEqual(get_layer(1), 0)
                self.assertEqual(get_layer(2), 1)
                self.assertEqual(get_layer(3), 1)
                self.assertEqual(get_layer(4), 1)
                self.assertEqual(get_layer(5), 1)
                self.assertEqual(get_layer(6), 1)
                self.assertEqual(get_layer(7), 1)
                self.assertEqual(get_layer(8), 1)
                self.assertEqual(get_layer(9), 1)
                self.assertEqual(get_layer(10), 2)
                self.assertEqual(get_layer(52), 4)
                self.assertEqual(get_layer(55), 4)
                self.assertEqual(get_layer(61), 4)
                self.assertEqual(get_layer(78), 4)
                self.assertEqual(get_layer(50), 4)

            def test_calculate_distance_should_work(self):
                d = calculate_distance(9)
                self.assertEqual(d, 2)

                d = calculate_distance(29)
                self.assertEqual(d, 4)

                d = calculate_distance(1)
                self.assertEqual(d, 0)

                d = calculate_distance(12)
                self.assertEqual(d, 3)

                d = calculate_distance(23)
                self.assertEqual(d, 2)

                d = calculate_distance(1024)
                self.assertEqual(d, 31)

        unittest.main()
    else:
        n = int(sys.argv[1])
        d = calculate_distance(n)
        print('The Manhattan Distance between %d to 1 is %s' % (n, d))
