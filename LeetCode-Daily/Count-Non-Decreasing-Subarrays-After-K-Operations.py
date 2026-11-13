# LeetCode 3420. Count Non-Decreasing Subarrays After K Operations (Hard)
#
# For each subarray, you may add 1 to any element, at most k times in total.
# Count the subarrays that can be made non-decreasing.
#
# The cheapest way to fix nums[l..r]: raise every element to the tallest one
# before it (its running max). cost(l, r) = sum of (running max - nums[i]).
#
# Grow every start:   for each l, extend r while the cost stays <= k. O(n^2).
# Two pointers:       cost only grows when the window grows on either side, so
#                     walk l from right to left and only ever move r left.
#                     Recomputing the cost each time is still slow.
# Blocks:             keep the window as blocks (target height, count). A new
#                     element on the left swallows the blocks it is taller than;
#                     dropping the right end shrinks the last block. O(n).
from collections import deque
from typing import List


class SolutionGrow:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        for l in range(n):
            top = 0
            cost = 0
            for r in range(l, n):
                top = max(top, nums[r])
                cost += top - nums[r]
                if cost > k:
                    break
                ans += 1
        return ans


class SolutionTwoPointers:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        def cost_of(l, r):
            top = total = 0
            for i in range(l, r + 1):
                top = max(top, nums[i])
                total += top - nums[i]
            return total

        n = len(nums)
        ans = 0
        r = n - 1
        for l in range(n - 1, -1, -1):
            while cost_of(l, r) > k:
                r -= 1
            ans += r - l + 1
        return ans


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        blocks = deque()
        cost = 0
        ans = 0
        r = n - 1
        for l in range(n - 1, -1, -1):
            v, cnt = nums[l], 1
            while blocks and blocks[0][0] <= v:
                bv, bc = blocks.popleft()
                cost += (v - bv) * bc
                cnt += bc
            blocks.appendleft([v, cnt])
            while cost > k:
                bv = blocks[-1][0]
                cost -= bv - nums[r]
                blocks[-1][1] -= 1
                if blocks[-1][1] == 0:
                    blocks.pop()
                r -= 1
            ans += r - l + 1
        return ans


def mistakes():
    def raise_to_previous(nums, k):
        # raises each element only to its left neighbour, not to the running max
        ans = 0
        for l in range(len(nums)):
            cost = 0
            for r in range(l, len(nums)):
                if r > l:
                    cost += max(0, nums[r - 1] - nums[r])
                if cost > k:
                    break
                ans += 1
        return ans

    def forward_drop_left(nums, k):
        # slides l forward, but when nums[l] leaves it only takes off nums[l]'s
        # own share; the elements after it keep targets raised by nums[l]
        n = len(nums); ans = 0; l = 0; cost = 0; top = 0; tgt = []
        for r in range(n):
            top = max(top, nums[r]); cost += top - nums[r]; tgt.append(top)
            while cost > k:
                cost -= tgt[l] - nums[l]; l += 1
                if l > r:
                    top = 0; break
            ans += r - l + 1
        return ans

    return raise_to_previous, forward_drop_left


if __name__ == "__main__":
    import random
    import time

    def every_subarray(nums, k):
        n = len(nums); ans = 0
        for l in range(n):
            for r in range(l, n):
                top = 0; cost = 0
                for i in range(l, r + 1):
                    top = max(top, nums[i]); cost += top - nums[i]
                ans += cost <= k
        return ans

    for nums, k, want in (([6, 3, 1, 2, 4, 4], 7, 17), ([6, 3, 1, 3, 6], 4, 12)):
        for s in (SolutionGrow(), SolutionTwoPointers(), Solution()):
            assert s.countNonDecreasingSubarrays(nums, k) == want, (type(s).__name__, nums, k)
    for _ in range(5000):
        nums = [random.randint(1, 9) for _ in range(random.randint(1, 9))]; k = random.randint(1, 15)
        want = every_subarray(nums, k)
        for s in (SolutionGrow(), SolutionTwoPointers(), Solution()):
            assert s.countNonDecreasingSubarrays(nums, k) == want, (type(s).__name__, nums, k)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            nums = [random.randint(1, 6) for _ in range(random.randint(1, 5))]; k = random.randint(1, 6)
            if f(nums, k) != Solution().countNonDecreasingSubarrays(nums, k):
                if found is None or (len(nums), sum(nums), k) < (len(found[0]), sum(found[0]), found[1]):
                    found = (nums, k)
        print(f.__name__, "fails on nums, k =", found, "->", f(*found), "instead of", Solution().countNonDecreasingSubarrays(*found)) if found else print(f.__name__, "found no failure")

    # worst case for the slow versions: a rising array, so every subarray costs 0
    nums = list(range(1, 3001))
    for s in (SolutionGrow(), SolutionTwoPointers(), Solution()):
        t0 = time.time(); s.countNonDecreasingSubarrays(nums, 1); print("rising, n = 3000:", type(s).__name__, f"{time.time() - t0:.3f}s")
    rnd = random.Random(5)
    for nums in (list(range(1, 10**5 + 1)), [rnd.randint(1, 10**9) for _ in range(10**5)]):
        for k in (1, 10**9):
            t0 = time.time(); Solution().countNonDecreasingSubarrays(nums, k); print(f"n = 100000, k = {k}: Solution {time.time() - t0:.3f}s")
