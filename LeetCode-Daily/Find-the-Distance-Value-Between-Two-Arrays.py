# LeetCode 1385. Find the Distance Value Between Two Arrays (Easy)
#
# Count the numbers a in arr1 that have no number b in arr2 with |a - b| <= d.
# Picture a "bubble" from a - d to a + d around each a. The bubble survives
# when no number of arr2 lands inside it (the edges count as inside).
#
# Slow way: check every pair.                     Time O(n * m), memory O(1)
# Fast way: sort arr2 once, then for each a use binary search to find the
#           first number >= a - d. Only that number can decide the bubble.
#                                                  Time O((n + m) log m), memory O(m)
from bisect import bisect_left
from typing import List


class SolutionSlow:
    def findTheDistanceValue(self, arr1: List[int], arr2: List[int], d: int) -> int:
        count = 0
        for a in arr1:
            ok = True
            for b in arr2:
                if abs(a - b) <= d:
                    ok = False
                    break
            if ok:
                count += 1
        return count


class Solution:
    def findTheDistanceValue(self, arr1: List[int], arr2: List[int], d: int) -> int:
        arr2 = sorted(arr2)
        count = 0
        for a in arr1:
            i = bisect_left(arr2, a - d)
            if i == len(arr2) or arr2[i] > a + d:
                count += 1
        return count


class SolutionTwoPointers:
    """Sort both arrays. As a grows, the first b >= a - d only moves right."""

    def findTheDistanceValue(self, arr1: List[int], arr2: List[int], d: int) -> int:
        arr2 = sorted(arr2)
        count = 0
        j = 0
        for a in sorted(arr1):
            while j < len(arr2) and arr2[j] < a - d:
                j += 1
            if j == len(arr2) or arr2[j] > a + d:
                count += 1
        return count


if __name__ == "__main__":
    import random

    cases = [
        ([4, 5, 8], [10, 9, 1, 8], 2, 2),
        ([1, 4, 2, 3], [-4, -3, 6, 10, 20, 30], 3, 2),
        ([2, 1, 100, 3], [-5, -2, 10, -3, 7], 6, 1),
        ([1, 5, 10], [8], 3, 1),
    ]
    sols = [SolutionSlow(), Solution(), SolutionTwoPointers()]
    for a1, a2, d, want in cases:
        assert all(s.findTheDistanceValue(a1, a2, d) == want for s in sols), (a1, a2, d)
    for _ in range(5000):
        a1 = [random.randint(-30, 30) for _ in range(random.randint(1, 12))]
        a2 = [random.randint(-30, 30) for _ in range(random.randint(1, 12))]
        d = random.randint(0, 10)
        want = SolutionSlow().findTheDistanceValue(a1, a2, d)
        assert Solution().findTheDistanceValue(a1, a2, d) == want, (a1, a2, d)
        assert SolutionTwoPointers().findTheDistanceValue(a1, a2, d) == want, (a1, a2, d)
    print("all tests pass")
