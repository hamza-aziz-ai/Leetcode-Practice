# LeetCode 55. Jump Game (Medium)
#
# You stand on stone 0. The number on each stone is the longest jump you may
# make from it (any shorter jump is fine too). Can you reach the last stone?
#
# Every path:     try every jump from every stone. Many paths land on the same
#                 stone and explore it again, so it blows up.
# Mark reachable: mark every stone each reachable stone can jump to. Each stone
#                 is explored once, but the same stones get marked again and
#                 again: O(n * jump length).
# Farthest reach: the reachable stones always form one solid stretch from
#                 stone 0, so one number says it all: far, the farthest stone
#                 reached so far. O(n) time, O(1) memory.
# Goal walks back: move the goal left whenever a stone can jump onto it.
from typing import List


class SolutionEveryPath:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)

        def go(i):
            if i >= n - 1:
                return True
            return any(go(i + step) for step in range(1, nums[i] + 1))
        return go(0)


class SolutionMark:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        reach = [False] * n
        reach[0] = True
        for i in range(n):
            if reach[i]:
                for j in range(i + 1, min(n, i + nums[i] + 1)):
                    reach[j] = True
        return reach[n - 1]


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        far = 0
        for i in range(len(nums)):
            if i > far:
                return False
            far = max(far, i + nums[i])
        return True


class SolutionGoal:
    def canJump(self, nums: List[int]) -> bool:
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0


def mistakes():
    def no_plus_one(nums):
        n = len(nums); reach = [False] * n; reach[0] = True
        for i in range(n):
            if reach[i]:
                for j in range(i + 1, min(n, i + nums[i])):
                    reach[j] = True
        return reach[n - 1]

    def no_min(nums):
        n = len(nums); reach = [False] * n; reach[0] = True
        try:
            for i in range(n):
                if reach[i]:
                    for j in range(i + 1, i + nums[i] + 1):
                        reach[j] = True
            return reach[n - 1]
        except IndexError as e:
            return f"IndexError: {e}"

    def update_first(nums):
        far = 0
        for i in range(len(nums)):
            far = max(far, i + nums[i])
            if i > far:
                return False
        return True

    def stop_at_zero(nums):
        goal = len(nums) - 1
        for i in range(len(nums) - 2, 0, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0

    print("range without + 1 on [1, 0] ->", no_plus_one([1, 0]), "instead of True")
    print("range without min on [3, 0, 0] ->", no_min([3, 0, 0]))
    print("update far before the check on [3, 2, 1, 0, 4] ->", update_first([3, 2, 1, 0, 4]), "instead of False")
    print("range(n - 2, 0, -1) on [1, 1] ->", stop_at_zero([1, 1]), "instead of True")


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionEveryPath(), SolutionMark(), Solution(), SolutionGoal())
    for nums, want in (([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False), ([0], True), ([2, 0, 2, 0, 1], True), ([1, 0], True), ([0, 1], False), ([2, 0, 0], True)):
        assert all(s.canJump(nums) == want for s in sols), nums
    for _ in range(5000):
        nums = [random.randint(0, 3) for _ in range(random.randint(1, 12))]
        want = SolutionEveryPath().canJump(nums)
        assert all(s.canJump(nums) == want for s in sols), nums
    print("all tests pass")
    mistakes()

    # Every path on a list that cannot reach the end: many paths, all stuck.
    for n in (20, 24, 28):
        nums = [3] * n + [0, 0, 0, 0]
        t = time.time(); r = SolutionEveryPath().canJump(nums); print(f"every path, {n} threes then four zeros:", r, f"{time.time() - t:.3f}s")
    # LeetCode's limits: up to 10,000 stones, numbers up to 100,000.
    nums = [10**5] * 10**4
    for s in sols[1:]:
        t = time.time(); s.canJump(nums); print("10,000 stones of 100,000:", type(s).__name__, f"{time.time() - t:.3f}s")
