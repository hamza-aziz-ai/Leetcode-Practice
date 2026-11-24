# LeetCode 3411. Maximum Subarray With Equal Products (Easy)
#
# A subarray is "product equivalent" if prod == lcm * gcd of its numbers. Return
# the length of the longest one. 2 <= n <= 100, 1 <= nums[i] <= 10.
#
# Every subarray, from scratch:  O(n^3).
# Grow each start:               keep a running product, gcd and lcm. O(n^2).
# Primes may not repeat:         count each prime p in a number. prod counts p
#     as often as all the numbers together; lcm * gcd counts it only as
#     (most in one number) + (fewest in one number). With 3 or more numbers
#     those agree only if at most one number holds p. So a long window is good
#     exactly when no prime (2, 3, 5, 7) appears in two of its numbers, and any
#     2 numbers are always good (a * b == lcm * gcd). Slide a window. O(4n).
from math import gcd, lcm, prod
from typing import List


class SolutionScratch:
    def maxLength(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            for j in range(i, n):
                sub = nums[i:j + 1]
                if prod(sub) == lcm(*sub) * gcd(*sub):
                    best = max(best, j - i + 1)
        return best


class SolutionGrow:
    def maxLength(self, nums: List[int]) -> int:
        n = len(nums)
        best = 0
        for i in range(n):
            p, g, l = 1, 0, 1
            for j in range(i, n):
                x = nums[j]
                p *= x
                g = gcd(g, x)
                l = lcm(l, x)
                if p == l * g:
                    best = max(best, j - i + 1)
        return best


class Solution:
    def maxLength(self, nums: List[int]) -> int:
        primes = [2, 3, 5, 7]
        last = {p: -1 for p in primes}
        best = 2
        left = 0
        for right, x in enumerate(nums):
            for p in primes:
                if x % p == 0:
                    left = max(left, last[p] + 1)
                    last[p] = right
            best = max(best, right - left + 1)
        return best


def mistakes():
    def coprime_neighbours(nums):
        # only checks neighbours, not every pair in the window
        best = 2; left = 0
        for r in range(1, len(nums)):
            if gcd(nums[r], nums[r - 1]) != 1:
                left = r
            best = max(best, r - left + 1)
        return best

    def start_best_at_one(nums):
        # forgets that any two numbers already work
        primes = [2, 3, 5, 7]; last = {p: -1 for p in primes}; best = 1; left = 0
        for right, x in enumerate(nums):
            for p in primes:
                if x % p == 0:
                    left = max(left, last[p] + 1); last[p] = right
            best = max(best, right - left + 1)
        return best

    def forget_max(nums):
        # moves left back when a prime was last seen before the window
        primes = [2, 3, 5, 7]; last = {p: -1 for p in primes}; best = 2; left = 0
        for right, x in enumerate(nums):
            for p in primes:
                if x % p == 0:
                    left = last[p] + 1; last[p] = right
            best = max(best, right - left + 1)
        return best

    return coprime_neighbours, start_best_at_one, forget_max


if __name__ == "__main__":
    import random
    import time

    for nums, want in (([1, 2, 1, 2, 1, 1, 1], 5), ([2, 3, 4, 5, 6], 3), ([1, 2, 3, 1, 4, 5, 1], 5)):
        for s in (SolutionScratch(), SolutionGrow(), Solution()):
            assert s.maxLength(nums) == want, (type(s).__name__, nums)
    for _ in range(5000):
        nums = [random.randint(1, 10) for _ in range(random.randint(2, 12))]
        want = SolutionScratch().maxLength(nums)
        for s in (SolutionGrow(), Solution()):
            assert s.maxLength(nums) == want, (type(s).__name__, nums)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            nums = [random.randint(1, 10) for _ in range(random.randint(2, 6))]
            if f(nums) != Solution().maxLength(nums) and (found is None or len(nums) < len(found)):
                found = nums
        print(f.__name__, "fails on", found, "->", f(found), "instead of", Solution().maxLength(found)) if found else print(f.__name__, "found no failure")

    nums = [1] * 100
    for s in (SolutionScratch(), SolutionGrow(), Solution()):
        t0 = time.time(); s.maxLength(nums); print("n = 100, all ones:", type(s).__name__, f"{time.time() - t0:.4f}s")
