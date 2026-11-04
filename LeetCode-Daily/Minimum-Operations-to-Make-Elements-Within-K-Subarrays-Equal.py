# LeetCode 3505. Minimum Operations to Make Elements Within K Subarrays Equal (Hard)
#
# Step 1: cost[s] = moves to make nums[s : s + x] all equal. The best common
#         value is the median, so the cost is the sum of distances to it.
#         Slide the window and keep its numbers split into two sorted halves,
#         `low` (smaller half) and `high` (bigger half), with their sums.
#         The median is low[-1], so each cost is found in O(log x).
# Step 2: dp[j][i] = cheapest way to build j groups using only nums[:i].
#         Either nums[i - 1] is not in the last group (skip), or the last
#         group is nums[i - x : i] (take).
# Time O(n log x + n * k), memory O(n * k).
from itertools import combinations
from typing import List

from sortedcontainers import SortedList


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Step 1: cost of every window of size x.
        low, high = SortedList(), SortedList()
        sum_low = sum_high = 0
        cost = [0] * (n - x + 1)
        for r in range(n):
            v = nums[r]
            if not low or v <= low[-1]:
                low.add(v)
                sum_low += v
            else:
                high.add(v)
                sum_high += v
            if r >= x:
                old = nums[r - x]
                if old <= low[-1]:
                    low.remove(old)
                    sum_low -= old
                else:
                    high.remove(old)
                    sum_high -= old
            while len(low) > len(high) + 1:
                m = low.pop()
                sum_low -= m
                high.add(m)
                sum_high += m
            while len(low) < len(high):
                m = high.pop(0)
                sum_high -= m
                low.add(m)
                sum_low += m
            if r >= x - 1:
                med = low[-1]
                cost[r - x + 1] = (med * len(low) - sum_low) + (sum_high - med * len(high))

        # Step 2: pick k groups that do not overlap.
        INF = float("inf")
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        for i in range(n + 1):
            dp[0][i] = 0
        for j in range(1, k + 1):
            for i in range(j * x, n + 1):
                skip = dp[j][i - 1]
                take = dp[j - 1][i - x] + cost[i - x]
                dp[j][i] = min(skip, take)
        return dp[k][n]


class SolutionTwoRows:
    """Same idea, but the dp table keeps only two rows: O(n) extra memory.

    Row j only ever reads row j - 1 (for take) and itself (for skip),
    so rows j - 2, j - 3, ... can be thrown away.
    """

    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        cost = window_costs(nums, x)
        INF = float("inf")
        prev = [0] * (n + 1)              # row j - 1; starts as row 0 (all zeros)
        for j in range(1, k + 1):
            cur = [INF] * (n + 1)         # row j
            for i in range(j * x, n + 1):
                skip = cur[i - 1]
                take = prev[i - x] + cost[i - x]
                cur[i] = min(skip, take)
            prev = cur                    # row j becomes "the row above" for j + 1
        return prev[n]


def window_costs(nums, x):
    """cost[s] for every window, using two Fenwick trees instead of SortedList.

    Values are swapped for their rank (0, 1, 2, ...). One tree counts how many
    window cards have each rank, the other adds up their values. The middle
    card is the (x // 2 + 1)-th smallest, found by walking down the tree.
    """
    vals = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)
    cnt = [0] * (m + 1)
    sm = [0] * (m + 1)

    def update(i, c, v):
        while i <= m:
            cnt[i] += c
            sm[i] += v
            i += i & -i

    def prefix(i):                        # count and sum of ranks 1..i
        c = t = 0
        while i > 0:
            c += cnt[i]
            t += sm[i]
            i -= i & -i
        return c, t

    def kth(need):                        # smallest rank whose prefix count >= need
        pos, step = 0, 1 << m.bit_length()
        while step:
            nxt = pos + step
            if nxt <= m and cnt[nxt] < need:
                pos = nxt
                need -= cnt[nxt]
            step >>= 1
        return pos + 1

    cost = []
    total = 0
    for r, v in enumerate(nums):
        update(rank[v], 1, v)
        total += v
        if r >= x:
            old = nums[r - x]
            update(rank[old], -1, -old)
            total -= old
        if r >= x - 1:
            med_rank = kth(x // 2 + 1)
            med = vals[med_rank - 1]
            c_le, s_le = prefix(med_rank)     # cards <= med
            cost.append((med * c_le - s_le) + (total - s_le - med * (x - c_le)))
    return cost


def min_ops_slow(nums, x, k):
    """Brute force: try every set of k groups that do not overlap."""
    def fix(group):
        g = sorted(group)
        mid = g[len(g) // 2]
        return sum(abs(v - mid) for v in g)

    best = float("inf")
    for starts in combinations(range(len(nums) - x + 1), k):
        if any(starts[t + 1] - starts[t] < x for t in range(k - 1)):
            continue
        best = min(best, sum(fix(nums[s:s + x]) for s in starts))
    return best


if __name__ == "__main__":
    import random

    sol = Solution()
    assert sol.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2) == 8
    assert sol.minOperations([9, -2, -2, -2, 1, 5], 2, 2) == 3
    for _ in range(3000):
        n = random.randint(2, 10)
        x = random.randint(2, n)
        k = random.randint(1, n // x)
        nums = [random.randint(-6, 6) for _ in range(n)]
        want = min_ops_slow(nums, x, k)
        assert sol.minOperations(nums, x, k) == want, (nums, x, k)
        assert SolutionTwoRows().minOperations(nums, x, k) == want, (nums, x, k)
    print("all tests pass")
