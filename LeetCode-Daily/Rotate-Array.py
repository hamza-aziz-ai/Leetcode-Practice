# LeetCode 189. Rotate Array (Medium)
#
# Rotate nums to the right by k steps, in place: the last k cards move to the
# front, keeping their order. k can be bigger than len(nums); rotating by n
# steps changes nothing, so only k % n steps matter.
#
# One step at a time: slide every card one spot right, k times. O(n * k).
# Jump straight there: card i belongs at spot (i + k) % n. Fill a new list,
#                      then copy it back. O(n) time, O(n) memory.
# Three reversals:     reverse the whole list, then reverse the first k cards,
#                      then the rest. O(n) time, O(1) memory.
from typing import List


class SolutionStep:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        for _ in range(k):
            last = nums[n - 1]
            for j in range(n - 1, 0, -1):
                nums[j] = nums[j - 1]
            nums[0] = last


class SolutionInsert:
    """The same one-step idea with list methods: shorter, still O(n * k)."""
    def rotate(self, nums: List[int], k: int) -> None:
        for _ in range(k % len(nums)):
            nums.insert(0, nums.pop())


class SolutionJump:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        new = [0] * n
        for i in range(n):
            new[(i + k) % n] = nums[i]
        nums[:] = new


class SolutionSlice:
    def rotate(self, nums: List[int], k: int) -> None:
        k %= len(nums)
        nums[:] = nums[-k:] + nums[:-k]


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        self.reverse(nums, 0, n - 1)
        self.reverse(nums, 0, k - 1)
        self.reverse(nums, k, n - 1)

    def reverse(self, nums: List[int], i: int, j: int) -> None:
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1


def expected(nums, k):
    n = len(nums)
    return [nums[(i - k) % n] for i in range(n)]


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionStep(), SolutionInsert(), SolutionJump(), SolutionSlice(), Solution())
    for nums, k, want in (([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]), ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
                          ([1, 2], 3, [2, 1]), ([7], 5, [7]), ([1, 2, 3], 0, [1, 2, 3])):
        for s in sols:
            arr = nums[:]
            s.rotate(arr, k)
            assert arr == want, (type(s).__name__, nums, k, arr)
    for _ in range(5000):
        nums = [random.randint(-9, 9) for _ in range(random.randint(1, 12))]
        k = random.randint(0, 30)
        for s in sols:
            arr = nums[:]
            s.rotate(arr, k)
            assert arr == expected(nums, k), (type(s).__name__, nums, k)
    print("all tests pass")

    # Mistakes shown on the page.
    a = [1, 2]; k = 3
    print("slices without k %= n on", a, "k = 3 ->", a[-k:] + a[:-k], "instead of", expected(a, k))
    a = [1, 2, 3, 4, 5, 6, 7]; b = a[:]
    r = Solution().reverse
    r(b, 0, 2); r(b, 3, 6); r(b, 0, 6)
    print("parts first, whole list last on", a, "k = 3 ->", b, "(that is a rotation to the left)")

    # LeetCode's biggest case: n = 100,000 and k up to 100,000.
    n = 100000
    big = list(range(n))
    for s, k, m in ((SolutionStep(), 300, n), (SolutionInsert(), n // 2 - 1, n), (SolutionJump(), n // 2 - 1, n), (SolutionSlice(), n // 2 - 1, n), (Solution(), n // 2 - 1, n)):
        arr = big[:m]
        t = time.time(); s.rotate(arr, k); dt = time.time() - t
        assert arr == expected(big[:m], k)
        print(f"n = {m}, k = {k}:", type(s).__name__, f"{dt:.3f}s")
