# LeetCode 3041. Maximize Consecutive Elements in an Array After Modification (Hard)
#
# First add 0 or 1 to each number. Then pick numbers whose values, sorted, are
# consecutive (3, 4, 5 yes; 3, 4, 6 or 1, 1, 2 no). Return the most you can pick.
#
# Every choice:   try all 2^n ways to add 0 or 1, and find the longest run of
#                 consecutive values in each. O(2^n * n log n).
# Sort, then dp:  sort; dp[v] = longest run of consecutive values that ends at
#                 value v, using the numbers seen so far. A number x can be x + 1
#                 (extending a run that ends at x) or x (extending one that ends
#                 at x - 1). Update x + 1 first, from the old dp[x]. O(n log n).
from itertools import product
from typing import List


def longest_run(vals):
    run = best = 0
    for v in sorted(vals):
        run = run + 1 if v - 1 in vals else 1
        best = max(best, run)
    return best


class SolutionEveryChoice:
    def maxSelectedElements(self, nums: List[int]) -> int:
        best = 0
        for adds in product((0, 1), repeat=len(nums)):
            vals = {x + a for x, a in zip(nums, adds)}
            best = max(best, longest_run(vals))
        return best


class Solution:
    def maxSelectedElements(self, nums: List[int]) -> int:
        nums.sort()
        dp = {}
        for x in nums:
            dp[x + 1] = dp.get(x, 0) + 1
            dp[x] = dp.get(x - 1, 0) + 1
        return max(dp.values())


def mistakes():
    def wrong_order(nums):
        # updates dp[x] first, so dp[x + 1] reads the new dp[x]: one number is used twice
        nums = sorted(nums); dp = {}
        for x in nums:
            dp[x] = dp.get(x - 1, 0) + 1
            dp[x + 1] = dp.get(x, 0) + 1
        return max(dp.values())

    def no_sort(nums):
        # same updates without sorting first
        dp = {}
        for x in nums:
            dp[x + 1] = dp.get(x, 0) + 1
            dp[x] = dp.get(x - 1, 0) + 1
        return max(dp.values())

    def raise_all_or_none(nums):
        # only tries adding 1 to every number or to none
        return max(longest_run(set(nums)), longest_run({x + 1 for x in nums}))

    return wrong_order, no_sort, raise_all_or_none


if __name__ == "__main__":
    import random
    import time

    for nums, want in (([2, 1, 5, 1, 1], 3), ([1, 4, 7, 10], 1)):
        for s in (SolutionEveryChoice(), Solution()):
            assert s.maxSelectedElements(nums[:]) == want, (type(s).__name__, nums)
    for _ in range(5000):
        nums = [random.randint(1, 8) for _ in range(random.randint(1, 8))]
        assert Solution().maxSelectedElements(nums[:]) == SolutionEveryChoice().maxSelectedElements(nums[:]), nums
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            nums = [random.randint(1, 5) for _ in range(random.randint(1, 5))]
            if f(nums[:]) != Solution().maxSelectedElements(nums[:]):
                if found is None or (len(nums), sum(nums)) < (len(found), sum(found)):
                    found = nums
        print(f.__name__, "fails on", found, "->", f(found[:]), "instead of", Solution().maxSelectedElements(found[:])) if found else print(f.__name__, "found no failure")

    for n in (14, 16, 18):
        nums = [random.randint(1, 20) for _ in range(n)]
        t0 = time.time(); SolutionEveryChoice().maxSelectedElements(nums[:]); print(f"n = {n}: SolutionEveryChoice {time.time() - t0:.3f}s")
    nums = [random.randint(1, 10**6) for _ in range(10**5)]
    t0 = time.time(); Solution().maxSelectedElements(nums[:]); print(f"n = 100000: Solution {time.time() - t0:.3f}s")
