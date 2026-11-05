# LeetCode 80. Remove Duplicates from Sorted Array II (Medium)
#
# nums is sorted. Keep at most two copies of each number, in place, and return
# k, how many cards are kept. The first k spots must hold them in the same
# order as before; whatever sits after spot k is ignored by the judge.
#
# Count in all kept:  build a new list `out`; add x when `out.count(x) < 2`.
#                     count() reads the whole of `out` every time: O(n * k).
# Look two back:      the list is sorted, so the copies of x already kept are
#                     the last cards of `out`. If out[-2] == x, then out[-1] == x
#                     too (it sits between them), so x would be a third copy.
#                     O(n) time, but O(n) extra memory.
# In place:           let the front of nums be `out`: k = len(out) and
#                     nums[k - 2] is out[-2]. O(n) time, O(1) memory.
# The same pattern keeps at most m copies: `k < m or nums[i] != nums[k - m]`.
# With m = 1 it is LeetCode 26.
from typing import List


class SolutionCountAll:
    def removeDuplicates(self, nums: List[int]) -> int:
        out = []
        for x in nums:
            if out.count(x) < 2:
                out.append(x)
        nums[:len(out)] = out
        return len(out)


class SolutionTwoBack:
    def removeDuplicates(self, nums: List[int]) -> int:
        out = []
        for x in nums:
            if len(out) < 2 or x != out[-2]:
                out.append(x)
        nums[:len(out)] = out
        return len(out)


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 0
        for i in range(len(nums)):
            if k < 2 or nums[i] != nums[k - 2]:
                nums[k] = nums[i]
                k += 1
        return k


def keep_at_most(nums: List[int], m: int) -> int:
    """The general form: keep at most m copies of each number."""
    k = 0
    for i in range(len(nums)):
        if k < m or nums[i] != nums[k - m]:
            nums[k] = nums[i]
            k += 1
    return k


class SolutionLookAtI:
    """A common mistake: compare with nums[i - 2], which may already be overwritten."""
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 0
        for i in range(len(nums)):
            if i < 2 or nums[i] != nums[i - 2]:
                nums[k] = nums[i]
                k += 1
        return k


def expected(nums):
    out = []
    for x in nums:
        if out[-2:] != [x, x]:
            out.append(x)
    return out


def judge(sol, nums):
    """The same check LeetCode runs: k must match, and nums[:k] must match in order."""
    want = expected(nums)
    arr = nums[:]
    k = sol.removeDuplicates(arr)
    return k == len(want) and arr[:k] == want and len(arr) == len(nums)


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionCountAll(), SolutionTwoBack(), Solution())
    for nums in ([1, 1, 1, 2, 2, 3], [0, 0, 1, 1, 1, 1, 2, 3, 3], [7], [5, 5, 5, 5, 5], [1, 2, 3, 4], [4, 4]):
        assert all(judge(s, nums) for s in sols), nums
    for _ in range(5000):
        nums = sorted(random.randint(-4, 4) for _ in range(random.randint(1, 15)))
        assert all(judge(s, nums) for s in sols), nums
        for m in (1, 2, 3):
            arr = nums[:]
            k = keep_at_most(arr, m)
            want = [x for i, x in enumerate(nums) if i < m or nums[i - m] != x]
            assert arr[:k] == want, (nums, m)
    print("all tests pass")

    bad = [1, 1, 1, 2, 2, 3]
    arr = bad[:]
    k = SolutionLookAtI().removeDuplicates(arr)
    print("nums[i - 2] mistake on", bad, "->", k, arr[:k], "instead of", len(expected(bad)), expected(bad))

    # LeetCode's numbers go from -10^4 to 10^4, so `out` can hold about 40,000
    # cards: out.count(x) is slow even within LeetCode's limits.
    for name, big in (("LeetCode-sized, random", sorted(random.randint(-10**4, 10**4) for _ in range(30000))),
                      ("30,000 different", list(range(30000)))):
        for s in sols:
            arr = big[:]
            t = time.time(); s.removeDuplicates(arr); print(name, type(s).__name__, f"{time.time() - t:.3f}s")
