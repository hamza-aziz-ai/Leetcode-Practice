# LeetCode 45. Jump Game II (Medium)
#
# Same stones as Jump Game: nums[i] is the longest jump from stone i. The last
# stone can always be reached. Return the fewest jumps that get you there.
#
# Every path:      try every jump, keep the fewest. Exponential.
# Fewest per stone: best[j] = fewest jumps to stone j. Each stone i offers
#                  best[i] + 1 to every stone it can land on. O(n * jump).
# Level by level:  the stones you can reach in exactly k jumps form one window.
#                  The next window runs from just after it to the farthest any
#                  of its stones can jump. Count windows. O(n).
# One pass:        the same windows in one loop: far grows stone by stone, and
#                  when i reaches the end of the current window, jump.
from typing import List


class SolutionEveryPath:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)

        def go(i):
            if i >= n - 1:
                return 0
            return min([go(i + s) + 1 for s in range(1, nums[i] + 1)], default=float("inf"))
        return go(0)


class SolutionFewestPerStone:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        best = [float("inf")] * n
        best[0] = 0
        for i in range(n):
            for j in range(i + 1, min(n, i + nums[i] + 1)):
                best[j] = min(best[j], best[i] + 1)
        return best[n - 1]


class SolutionLevels:
    def jump(self, nums: List[int]) -> int:
        n = len(nums)
        jumps, lo, hi = 0, 0, 0
        while hi < n - 1:
            far = max(i + nums[i] for i in range(lo, hi + 1))
            lo, hi = hi + 1, far
            jumps += 1
        return jumps


class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps, end, far = 0, 0, 0
        for i in range(len(nums) - 1):
            far = max(far, i + nums[i])
            if i == end:
                jumps += 1
                end = far
        return jumps


def mistakes():
    def whole_range(nums):
        jumps, end, far = 0, 0, 0
        for i in range(len(nums)):
            far = max(far, i + nums[i])
            if i == end:
                jumps += 1
                end = far
        return jumps

    def check_first(nums):
        jumps, end, far = 0, 0, 0
        for i in range(len(nums) - 1):
            if i == end:
                jumps += 1
                end = far
            far = max(far, i + nums[i])
        return jumps

    def farthest_landing(nums):
        i, jumps = 0, 0
        while i < len(nums) - 1:
            if nums[i] == 0:
                return "stuck on stone %d" % i
            i = min(len(nums) - 1, i + nums[i])
            jumps += 1
        return jumps

    print("range(len(nums)) on [2, 3, 1, 1, 4] ->", whole_range([2, 3, 1, 1, 4]), "instead of 2; on [0] ->", whole_range([0]), "instead of 0")
    print("check before far on [2, 3, 1, 1, 4] ->", check_first([2, 3, 1, 1, 4]), "instead of 2")
    print("always land as far as you can on [2, 3, 1, 1, 4] ->", farthest_landing([2, 3, 1, 1, 4]), "instead of 2")
    print("always land as far as you can on [2, 3, 0, 1, 4] ->", farthest_landing([2, 3, 0, 1, 4]))


def can_reach(nums):
    far = 0
    for i, v in enumerate(nums):
        if i > far:
            return False
        far = max(far, i + v)
    return True


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionEveryPath(), SolutionFewestPerStone(), SolutionLevels(), Solution())
    for nums, want in (([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([0], 0), ([1, 2, 1, 1, 1], 3), ([1, 1], 1)):
        assert all(s.jump(nums) == want for s in sols), nums
    tested = 0
    while tested < 5000:
        nums = [random.randint(0, 4) for _ in range(random.randint(1, 12))]
        if not can_reach(nums):
            continue
        tested += 1
        want = SolutionEveryPath().jump(nums)
        assert all(s.jump(nums) == want for s in sols), nums
    print("all tests pass")
    mistakes()

    for n in (18, 22, 26):
        nums = [3] * n
        t = time.time(); SolutionEveryPath().jump(nums); print(f"every path, {n} stones of 3:", f"{time.time() - t:.3f}s")
    # LeetCode's limits: up to 10,000 stones, numbers up to 1,000.
    nums = [1000] * 10**4
    for s in sols[1:]:
        t = time.time(); r = s.jump(nums); print("10,000 stones of 1,000:", type(s).__name__, r, f"{time.time() - t:.3f}s")
