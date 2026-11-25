# LeetCode 3934. Smallest Unique Subarray (Medium)
#
# Return the smallest length L such that some subarray of length L appears
# exactly once in nums (no other subarray has the same elements in order).
#
# Try every length:     L = 1, 2, ...; count every window of length L as a
#                       tuple; stop at the first L with a count of 1. O(n^2 L).
# Binary search on L:   if a window of length L is unique, any longer window
#                       that contains it is unique too, so "some window of
#                       length L is unique" is False ... False True ... True.
#                       Binary search for the first True. Tuples still cost L.
# Rolling hash:         slide a hash over the windows so each costs O(1).
#                       O(n log n). A 61-bit modulus with a random base makes
#                       two different windows getting the same hash vanishingly
#                       unlikely.
import random
from collections import Counter
from typing import List


class SolutionEveryLength:
    def smallestUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        for L in range(1, n + 1):
            seen = Counter(tuple(nums[i:i + L]) for i in range(n - L + 1))
            if 1 in seen.values():
                return L
        return n


class SolutionBinaryTuples:
    def smallestUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)

        def has_unique(L):
            seen = Counter(tuple(nums[i:i + L]) for i in range(n - L + 1))
            return 1 in seen.values()

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if has_unique(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


class Solution:
    def smallestUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        mod = (1 << 61) - 1
        base = random.randrange(10**6, mod - 1)
        pre = [0] * (n + 1)
        pw = [1] * (n + 1)
        for i, x in enumerate(nums):
            pre[i + 1] = (pre[i] * base + x) % mod
            pw[i + 1] = pw[i] * base % mod

        def has_unique(L):
            seen = Counter((pre[i + L] - pre[i] * pw[L]) % mod for i in range(n - L + 1))
            return 1 in seen.values()

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if has_unique(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


def mistakes():
    def count_distinct(nums):
        # asks for a length where all windows are different, not one window that is unique
        n = len(nums)
        for L in range(1, n + 1):
            w = [tuple(nums[i:i + L]) for i in range(n - L + 1)]
            if len(set(w)) == len(w):
                return L
        return n

    def sum_hash(nums):
        # "hashes" a window by its sum, so [1, 2] and [2, 1] look the same
        n = len(nums)
        for L in range(1, n + 1):
            seen = Counter(sum(nums[i:i + L]) for i in range(n - L + 1))
            if 1 in seen.values():
                return L
        return n

    def binary_search_wrong_side(nums):
        # moves the wrong bound: keeps searching longer when mid already works
        n = len(nums); lo, hi = 1, n
        def has_unique(L):
            return 1 in Counter(tuple(nums[i:i + L]) for i in range(n - L + 1)).values()
        while lo < hi:
            mid = (lo + hi) // 2
            if has_unique(mid):
                lo = mid + 1
            else:
                hi = mid
        return lo

    return count_distinct, sum_hash, binary_search_wrong_side


if __name__ == "__main__":
    import time

    for nums, want in (([3, 3, 3], 3), ([2, 1, 2, 3, 3], 1), ([1, 1, 2, 2, 1], 2)):
        for s in (SolutionEveryLength(), SolutionBinaryTuples(), Solution()):
            assert s.smallestUniqueSubarray(nums) == want, (type(s).__name__, nums)
    # the claim behind the binary search: once some length has a unique window, every longer one does too
    for _ in range(3000):
        nums = [random.randint(1, 3) for _ in range(random.randint(1, 12))]
        n = len(nums)
        flags = [1 in Counter(tuple(nums[i:i + L]) for i in range(n - L + 1)).values() for L in range(1, n + 1)]
        assert flags == sorted(flags), (nums, flags)
    for _ in range(5000):
        nums = [random.randint(1, random.choice([2, 3, 5])) for _ in range(random.randint(1, 14))]
        want = SolutionEveryLength().smallestUniqueSubarray(nums)
        for s in (SolutionBinaryTuples(), Solution()):
            assert s.smallestUniqueSubarray(nums) == want, (type(s).__name__, nums)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            nums = [random.randint(1, 3) for _ in range(random.randint(1, 6))]
            if f(nums) != Solution().smallestUniqueSubarray(nums) and (found is None or len(nums) < len(found)):
                found = nums
        print(f.__name__, "fails on", found, "->", f(found), "instead of", Solution().smallestUniqueSubarray(found)) if found else print(f.__name__, "found no failure")

    for name, nums in (("all equal, n = 2000", [7] * 2000), ("all equal, n = 100000", [7] * 100000), ("random 1..3, n = 100000", [random.randint(1, 3) for _ in range(100000)])):
        for s in (SolutionEveryLength(), SolutionBinaryTuples(), Solution()):
            if len(nums) > 2000 and not isinstance(s, Solution):
                continue
            t0 = time.time(); r = s.smallestUniqueSubarray(nums); print(f"{name}:", type(s).__name__, f"{time.time() - t0:.3f}s", "->", r)
