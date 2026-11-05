# LeetCode 88. Merge Sorted Array (Easy)
#
# nums1 holds m sorted numbers followed by n empty spots (zeros). nums2 holds n
# sorted numbers. Put all m + n numbers into nums1, sorted, without returning.
#
# Stop 2, sort:        drop nums2 into the empty spots, then sort everything.
#                      O((m + n) log(m + n)) time. Ignores that both parts are sorted.
# Stop 3, front merge: copy nums1's numbers, then zip the copy and nums2 together
#                      from the front. O(m + n) time, but O(m) extra memory.
# Stop 4, back merge:  zip from the back, biggest first, straight into the empty
#                      spots. O(m + n) time and O(1) extra memory.
from typing import List


class SolutionSort:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        nums1[m:] = nums2
        nums1.sort()


class SolutionFront:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        first = nums1[:m]
        i, j, k = 0, 0, 0
        while i < m and j < n:
            if first[i] <= nums2[j]:
                nums1[k] = first[i]
                i += 1
            else:
                nums1[k] = nums2[j]
                j += 1
            k += 1
        while i < m:
            nums1[k] = first[i]
            i += 1
            k += 1
        while j < n:
            nums1[k] = nums2[j]
            j += 1
            k += 1


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, k = m - 1, n - 1, m + n - 1
        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]), ([1], 1, [], 0, [1]), ([0], 0, [1], 1, [1])]
    sols = (SolutionSort(), SolutionFront(), Solution())
    for a, m, b, n, want in cases:
        for s in sols:
            x = a[:]
            assert s.merge(x, m, b[:], n) is None and x == want, (type(s).__name__, a, b)
    for _ in range(5000):
        m, n = random.randint(0, 9), random.randint(0, 9)
        if m + n == 0:
            continue
        a = sorted(random.randint(-9, 9) for _ in range(m)) + [0] * n
        b = sorted(random.randint(-9, 9) for _ in range(n))
        want = sorted(a[:m] + b)
        for s in sols:
            x = a[:]
            s.merge(x, m, b[:], n)
            assert x == want, (type(s).__name__, a, m, b, n, x)
    print("all tests pass")
