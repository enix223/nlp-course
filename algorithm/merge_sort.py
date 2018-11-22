#!/usr/local/env python

"""
==========
Merge Sort
==========

MERGE(A, p, q, r)
n1 = q - p + 1
n2 = r - q
let L[1..n1 + 1] and R[1..n2 + 1] be new arrays
for i = 1 to n1
    L[i] = A[p + i - 1]
for j = 1 to n2
    R[j] = A[q + 1]
L[n1 + 1] = infinite
R[n2 + 1] = infinite
i = 1
j = 1
for k = p to r
    if L[i] <= R[j]
        A[k] = L[i]
        i = i + 1
    else
        A[k] = R[j]
        j = j + 1

MERGE-SORT(A, p, r)
if p < r
    q = [(p + r) / 2]
    MERGE-SORT(A, p, q)
    MERGE-SORT(A, q + 1, r)
    MERGE(A, p, q, r)

Example:
==========

2 4 5 7 1 2 3 6
"""


def merge(A, p, q, r):
    r"""
    Merge two sorted array into one sorted array

    :param list A: The origin list
    :param int p:  The start index of the left array
    :param int q:  The end index of the left array
    :param int r:  The end index of the right array

       ------------------------------
    A  |..... | Left | Right |......|
       ------------------------------
              ^      ^       ^
              |      |       |
              p      q       r

    Example:
      |1 2 2 3 4 5 6|
       /          \
    |2 4 5|  |1 2 3 6|
     |   |    |     |
     p   q   q+1    r
    """
    left, right = [], []
    for i in range(p, q + 1):
        left.append(A[i])

    for j in range(q + 1, r + 1):
        right.append(A[j])

    i, j = 0, 0
    for k in range(p, r + 1):
        if i > q - p:
            A[k] = right[j]
            j += 1
            continue
        if j > r - q - 1:
            A[k] = left[i]
            i += 1
            continue

        if left[i] <= right[j]:
            A[k] = left[i]
            i += 1
        else:
            A[k] = right[j]
            j += 1


def merge_sort(A, p, r):
    if p < r:
        q = int((r + p) / 2)
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)


if __name__ == '__main__':
    # Test merge
    A = [1, 2, 4, 5, 6, 1, 2, 3, 6, 9, 11]
    merge(A, 2, 4, 7)
    assert A == [1, 2, 1, 2, 3, 4, 5, 6, 6, 9, 11], A

    A = [1, 2, 4, 5, 1, 2, 3, 6, 9, 11]
    merge(A, 1, 3, 7)
    assert A == [1, 1, 2, 2, 3, 4, 5, 6, 9, 11], A

    A = [1, 2, 4, 1, 2, 3, 6, 9, 11]
    merge(A, 0, 2, 8)
    assert A == [1, 1, 2, 2, 3, 4, 6, 9, 11], A

    # Test merge sort
    A = [1, 2, 4, 1, 2, 3, 6, 9, 11]
    merge_sort(A, 0, len(A) - 1)
    assert A == [1, 1, 2, 2, 3, 4, 6, 9, 11], A

    # Test merge sort
    A = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    merge_sort(A, 0, len(A) - 1)
    assert A == [1, 2, 3, 4, 5, 6, 7, 8, 9], A
