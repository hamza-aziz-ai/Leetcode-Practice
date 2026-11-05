# LeetCode 169. Majority Element (Easy)
#
# One number fills more than half of nums (more than n // 2 cards). Return it.
# The problem promises that such a number exists.
#
# Count each card:  for every x, nums.count(x) reads the whole list. O(n^2).
# Tally once:       a dictionary keeps one running count per number, so each
#                   card is read once. O(n) time, but O(n) memory.
# Vote (Boyer-Moore): keep one candidate and a count. A card equal to the
#                   candidate adds one; any other card knocks one out. When the
#                   count hits 0, the next card becomes the candidate. The
#                   majority has more cards than all the others together, so it
#                   cannot be knocked out completely. O(n) time, O(1) memory.
#                   It needs the promise: on [1, 2, 3] it returns 3.
from collections import Counter
from typing import List


class SolutionCount:
    def majorityElement(self, nums: List[int]) -> int:
        half = len(nums) // 2
        for x in nums:
            if nums.count(x) > half:
                return x


class SolutionTally:
    def majorityElement(self, nums: List[int]) -> int:
        half = len(nums) // 2
        counts = {}
        for x in nums:
            counts[x] = counts.get(x, 0) + 1
            if counts[x] > half:
                return x


class SolutionSort:
    def majorityElement(self, nums: List[int]) -> int:
        # The majority covers more than half the spots, so it covers the middle one.
        return sorted(nums)[len(nums) // 2]


class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate, count = None, 0
        for x in nums:
            if count == 0:
                candidate = x
            if x == candidate:
                count += 1
            else:
                count -= 1
        return candidate


def make(n, maj, rnd):
    """A list of n numbers where maj fills more than half."""
    m = n // 2 + 1 + rnd.randint(0, (n - 1) // 2)
    m = min(m, n)
    rest = [rnd.choice([v for v in range(-3, 4) if v != maj]) for _ in range(n - m)]
    arr = [maj] * m + rest
    rnd.shuffle(arr)
    return arr


if __name__ == "__main__":
    import random
    import time

    rnd = random.Random(1)
    sols = (SolutionCount(), SolutionTally(), SolutionSort(), Solution())
    for nums, want in (([3, 2, 3], 3), ([2, 2, 1, 1, 1, 2, 2], 2), ([7], 7), ([4, 4, 1, 5, 5, 5, 5], 5), ([9, 9, 9, 1, 2], 9)):
        assert all(s.majorityElement(nums[:]) == want for s in sols), nums
    for _ in range(5000):
        n = rnd.randint(1, 15)
        maj = rnd.randint(-3, 3)
        nums = make(n, maj, rnd)
        assert all(s.majorityElement(nums[:]) == maj for s in sols), nums
        assert Counter(nums).most_common(1)[0][0] == maj
    print("all tests pass")
    print("vote without the promise, [1, 2, 3] ->", Solution().majorityElement([1, 2, 3]))

    # Worst case for counting each card: the other numbers come first, all
    # different, so each of them costs a full count of the list.
    n = 50000
    worst = list(range(1, n // 2)) + [0] * (n - n // 2 + 1)
    worst = worst[:n]
    assert worst.count(0) > n // 2
    for s in sols:
        t = time.time(); s.majorityElement(worst[:]); print("LeetCode max n, majority last:", type(s).__name__, f"{time.time() - t:.3f}s")
