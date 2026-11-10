# LeetCode 3693. Climbing Stairs II (Medium)
#
# Steps 0..n. From step i you may jump to i + 1, i + 2 or i + 3. Landing on step
# j from step i costs costs[j] + (j - i)^2 (costs is 1-indexed in the statement,
# so in Python it is costs[j - 1]). Start on step 0 with cost 0. Return the
# cheapest total cost to reach step n.
#
# Try every path:  reach(j) = cheapest way to stand on step j; it tries the
#                  three steps it could have come from. Exponential.
# Table:           dp[j] for every step, filled from the bottom. O(n).
# Three numbers:   dp[j] needs only the last three values. O(n), O(1) memory.
from typing import List


class SolutionAllPaths:
    def climbStairs(self, n: int, costs: List[int]) -> int:
        def reach(j):
            if j == 0:
                return 0
            res = float("inf")
            for i in range(max(0, j - 3), j):
                res = min(res, reach(i) + (j - i) ** 2)
            return res + costs[j - 1]

        return reach(n)


class SolutionTable:
    def climbStairs(self, n: int, costs: List[int]) -> int:
        dp = [0] * (n + 1)
        for j in range(1, n + 1):
            best = float("inf")
            for i in range(max(0, j - 3), j):
                best = min(best, dp[i] + (j - i) ** 2)
            dp[j] = best + costs[j - 1]
        return dp[n]


class Solution:
    # a, b, c = cheapest cost to reach steps j - 3, j - 2, j - 1. Steps -2 and -1
    # do not exist, so they start at infinity. (Starting them at 0 happens to
    # give the same answers: a jump from a pretend step is always longer, so
    # dearer, than the same landing from step 0. Infinity says what we mean.)
    def climbStairs(self, n: int, costs: List[int]) -> int:
        a, b, c = float("inf"), float("inf"), 0
        for j in range(1, n + 1):
            d = min(c + 1, b + 4, a + 9) + costs[j - 1]
            a, b, c = b, c, d
        return c


def mistakes():
    def greedy(n, costs):
        # always takes the cheapest single jump from where it stands
        i = tot = 0
        while i < n:
            j = min(range(i + 1, min(i + 3, n) + 1), key=lambda j: costs[j - 1] + (j - i) ** 2)
            tot += costs[j - 1] + (j - i) ** 2; i = j
        return tot

    def no_square(n, costs):
        # jump cost (j - i) instead of (j - i) ** 2
        dp = [0] * (n + 1)
        for j in range(1, n + 1):
            dp[j] = min(dp[i] + (j - i) for i in range(max(0, j - 3), j)) + costs[j - 1]
        return dp[n]

    return greedy, no_square


if __name__ == "__main__":
    import random
    import time
    from itertools import product

    def every_path(n, costs):
        best = float("inf")
        for jumps in product((1, 2, 3), repeat=n):
            i = tot = 0
            for s in jumps:
                if i == n:
                    break
                if i + s > n:
                    tot = None; break
                tot += costs[i + s - 1] + s * s; i += s
            if tot is not None and i == n:
                best = min(best, tot)
        return best

    for n, costs, want in ((4, [1, 2, 3, 4], 13), (4, [5, 1, 6, 2], 11), (3, [9, 8, 3], 12)):
        for s in (SolutionAllPaths(), SolutionTable(), Solution()):
            assert s.climbStairs(n, costs) == want, (type(s).__name__, n, costs)
    for _ in range(3000):
        n = random.randint(1, 8); costs = [random.randint(1, 20) for _ in range(n)]
        want = every_path(n, costs)
        for s in (SolutionAllPaths(), SolutionTable(), Solution()):
            assert s.climbStairs(n, costs) == want, (type(s).__name__, n, costs)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            n = random.randint(1, 5); costs = [random.randint(1, 9) for _ in range(n)]
            if f(n, costs) != Solution().climbStairs(n, costs):
                if found is None or (n, sum(costs)) < (found[0], sum(found[1])):
                    found = (n, costs)
        print(f.__name__, "fails on n, costs =", found, "->", f(*found), "instead of", Solution().climbStairs(*found)) if found else print(f.__name__, "found no failure")

    for n in (20, 24, 26):
        costs = [random.randint(1, 10**4) for _ in range(n)]
        t0 = time.time(); SolutionAllPaths().climbStairs(n, costs); print(f"n = {n}: SolutionAllPaths {time.time() - t0:.3f}s")
    costs = [random.randint(1, 10**4) for _ in range(10**5)]
    for s in (SolutionTable(), Solution()):
        t0 = time.time(); s.climbStairs(10**5, costs); print("n = 100000:", type(s).__name__, f"{time.time() - t0:.3f}s")
