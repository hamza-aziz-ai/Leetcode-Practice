# LeetCode 15. 3Sum (Medium)
#
# Return every triplet [nums[i], nums[j], nums[k]] with i, j, k all different
# and a sum of 0. No triplet may appear twice (as a set of values).
#
# Every triple:        three loops, keep each triplet sorted in a set. O(n^3).
# Fix one, Two Sum:    fix nums[i]; for the rest, ask a set whether the third
#                      number needed was already seen. O(n^2), plus set space.
# Sort, two pointers:  sort; fix nums[i]; walk lo up and hi down, moving the one
#                      that brings the sum toward 0. Skip equal values so each
#                      triplet appears once, with no set. O(n^2), O(1) extra.
from typing import List


class SolutionEveryTriple:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        found = set()
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
        return [list(t) for t in found]


class SolutionTwoSum:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        found = set()
        for i in range(n):
            seen = set()
            for j in range(i + 1, n):
                need = -nums[i] - nums[j]
                if need in seen:
                    found.add(tuple(sorted((nums[i], nums[j], need))))
                seen.add(nums[j])
        return [list(t) for t in found]


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        ans = []
        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s < 0:
                    lo += 1
                elif s > 0:
                    hi -= 1
                else:
                    ans.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
        return ans


def mistakes():
    def no_skip_i(nums):
        # forgets to skip a first number equal to the one before it
        nums = sorted(nums); n = len(nums); ans = []
        for i in range(n - 2):
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s < 0: lo += 1
                elif s > 0: hi -= 1
                else:
                    ans.append([nums[i], nums[lo], nums[hi]]); lo += 1; hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]: lo += 1
        return ans

    def no_skip_lo(nums):
        # after a find, moves on without skipping equal values of lo
        nums = sorted(nums); n = len(nums); ans = []
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]: continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s < 0: lo += 1
                elif s > 0: hi -= 1
                else:
                    ans.append([nums[i], nums[lo], nums[hi]]); lo += 1; hi -= 1
        return ans

    def stop_at_zero(nums):
        # breaks when nums[i] >= 0, so [0, 0, 0] is never found
        nums = sorted(nums); n = len(nums); ans = []
        for i in range(n - 2):
            if nums[i] >= 0: break
            if i > 0 and nums[i] == nums[i - 1]: continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s < 0: lo += 1
                elif s > 0: hi -= 1
                else:
                    ans.append([nums[i], nums[lo], nums[hi]]); lo += 1; hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]: lo += 1
        return ans

    def skip_i_forward(nums):
        # skips nums[i] when it equals the NEXT number, which loses [-1, -1, 2]
        nums = sorted(nums); n = len(nums); ans = []
        for i in range(n - 2):
            if nums[i] == nums[i + 1]: continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s < 0: lo += 1
                elif s > 0: hi -= 1
                else:
                    ans.append([nums[i], nums[lo], nums[hi]]); lo += 1; hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]: lo += 1
        return ans

    return no_skip_i, no_skip_lo, stop_at_zero, skip_i_forward


if __name__ == "__main__":
    import random
    import time

    norm = lambda res: sorted(map(tuple, (sorted(t) for t in res)))
    exact = lambda res: sorted(map(tuple, res))  # keeps duplicates, so a repeated triplet shows

    for nums, want in (([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]), ([0, 1, 1], []), ([0, 0, 0], [[0, 0, 0]])):
        for s in (SolutionEveryTriple(), SolutionTwoSum(), Solution()):
            got = s.threeSum(nums[:])
            assert exact(got) == norm(want) and len(got) == len(set(map(tuple, got))), (type(s).__name__, nums, got)
    for _ in range(5000):
        nums = [random.randint(-5, 5) for _ in range(random.randint(3, 10))]
        want = norm(SolutionEveryTriple().threeSum(nums[:]))
        for s in (SolutionTwoSum(), Solution()):
            got = s.threeSum(nums[:])
            assert sorted(map(tuple, (sorted(t) for t in got))) == want and len(got) == len(want), (type(s).__name__, nums, got)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            nums = [random.randint(-3, 3) for _ in range(random.randint(3, 6))]
            got = f(nums[:])
            if sorted(map(tuple, (sorted(t) for t in got))) != norm(Solution().threeSum(nums[:])):
                if found is None or len(nums) < len(found):
                    found = nums
        print(f.__name__, "fails on", found, "->", f(found[:]), "instead of", Solution().threeSum(found[:])) if found else print(f.__name__, "found no failure")

    rnd = random.Random(3)
    for n in (200, 400):
        nums = [rnd.randint(-10**5, 10**5) for _ in range(n)]
        t0 = time.time(); SolutionEveryTriple().threeSum(nums[:]); print(f"n = {n}: SolutionEveryTriple {time.time() - t0:.3f}s")
    nums = [rnd.randint(-10**5, 10**5) for _ in range(3000)]
    for s in (SolutionTwoSum(), Solution()):
        t0 = time.time(); s.threeSum(nums[:]); print("n = 3000:", type(s).__name__, f"{time.time() - t0:.3f}s")
    nums = [rnd.randint(-50, 50) for _ in range(3000)]
    for s in (SolutionTwoSum(), Solution()):
        t0 = time.time(); s.threeSum(nums[:]); print("n = 3000, values -50..50:", type(s).__name__, f"{time.time() - t0:.3f}s")
