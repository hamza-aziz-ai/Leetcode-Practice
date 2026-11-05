# LeetCode 26. Remove Duplicates from Sorted Array (Easy)
#
# nums is sorted. Keep one copy of each number, in place, and return k, how many
# different numbers there are. The first k spots must hold them in the same
# order as before; whatever sits after spot k is ignored by the judge.
#
# Check all kept:   build a new list `out`; add x when `x not in out`.
#                   `in` walks the whole of `out`, so it is O(n * k).
# Check last kept:  the list is sorted, so copies sit next to each other.
#                   Only compare x with out[-1]. O(n) time, but O(n) extra memory.
# In place:         let the front of nums be `out`. k = len(out), nums[k - 1] is
#                   out[-1], and "append" is nums[k] = nums[i]; k += 1.
#                   O(n) time, O(1) memory.
from typing import List


class SolutionCheckAll:
    def removeDuplicates(self, nums: List[int]) -> int:
        out = []
        for x in nums:
            if x not in out:
                out.append(x)
        nums[:len(out)] = out
        return len(out)


class SolutionCheckLast:
    def removeDuplicates(self, nums: List[int]) -> int:
        out = []
        for x in nums:
            if not out or x != out[-1]:
                out.append(x)
        nums[:len(out)] = out
        return len(out)


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[k - 1]:
                nums[k] = nums[i]
                k += 1
        return k


def judge(sol, nums):
    """The same check LeetCode runs: k must match, and nums[:k] must match in order."""
    expected = sorted(set(nums))
    arr = nums[:]
    k = sol.removeDuplicates(arr)
    return k == len(expected) and arr[:k] == expected and len(arr) == len(nums)


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionCheckAll(), SolutionCheckLast(), Solution())
    for nums in ([1, 1, 2], [0, 0, 1, 1, 1, 2, 2, 3, 3, 4], [5], [5, 5, 5, 5], [1, 2, 3, 4], [-100, -100, 100]):
        assert all(judge(s, nums) for s in sols), nums
    for _ in range(5000):
        nums = sorted(random.randint(-5, 5) for _ in range(random.randint(1, 15)))
        assert all(judge(s, nums) for s in sols), nums
    print("all tests pass")

    # LeetCode's lists have at most 30,000 numbers from -100 to 100, so at most
    # 201 different numbers: `x not in out` is short there. With many different
    # numbers it shows its O(n * k) cost.
    for name, big in (("201 different (LeetCode's limit)", sorted(random.randint(-100, 100) for _ in range(30000))),
                      ("30,000 different", list(range(30000)))):
        for s in sols:
            arr = big[:]
            t = time.time(); s.removeDuplicates(arr); print(name, type(s).__name__, f"{time.time() - t:.3f}s")
