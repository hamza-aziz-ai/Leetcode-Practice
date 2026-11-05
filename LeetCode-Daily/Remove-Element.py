# LeetCode 27. Remove Element (Easy)
#
# Remove every copy of val from nums in place and return k, how many numbers
# are left. The first k spots must hold those numbers (in any order); whatever
# sits after spot k is ignored by the judge.
#
# Slow way:      while val in nums: nums.remove(val)
#                Each remove searches and then shifts every later number left,
#                so it is O(n^2) in the worst case.
# Reader/writer: i reads every number once; k marks where the next keeper goes.
#                O(n) time, O(1) memory, keeps the order. Writes once per keeper.
# Swap from end: when nums[i] == val, drop the last number on top of it and
#                shrink the list. O(n) time, O(1) memory, writes once per
#                removed number, but the order changes.
from typing import List


class SolutionRemove:
    def removeElement(self, nums: List[int], val: int) -> int:
        while val in nums:
            nums.remove(val)
        return len(nums)


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k


class SolutionSwap:
    def removeElement(self, nums: List[int], val: int) -> int:
        i, n = 0, len(nums)
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n - 1]
                n -= 1
            else:
                i += 1
        return n


def judge(sol, nums, val):
    """The same check LeetCode runs: k must match, and the first k (sorted) must match."""
    expected = sorted(x for x in nums if x != val)
    arr = nums[:]
    k = sol.removeElement(arr, val)
    return k == len(expected) and sorted(arr[:k]) == expected


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionRemove(), Solution(), SolutionSwap())
    for nums, val in [([3, 2, 2, 3], 3), ([0, 1, 2, 2, 3, 0, 4, 2], 2), ([], 1), ([7, 7, 7], 7), ([1, 2, 3], 4)]:
        assert all(judge(s, nums, val) for s in sols), (nums, val)
    for _ in range(5000):
        nums = [random.randint(0, 5) for _ in range(random.randint(0, 15))]
        val = random.randint(0, 6)
        assert all(judge(s, nums, val) for s in sols), (nums, val)
    print("all tests pass")

    # LeetCode's lists have at most 100 numbers, so every way is instant there.
    # On a long list the remove() loop shows its O(n^2) cost.
    big = [random.choice([0, 1]) for _ in range(40000)]
    for s in sols:
        arr = big[:]
        t = time.time(); s.removeElement(arr, 0); print(type(s).__name__, f"{time.time() - t:.2f}s")
