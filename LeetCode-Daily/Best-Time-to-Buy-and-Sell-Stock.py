# LeetCode 121. Best Time to Buy and Sell Stock (Easy)
#
# prices[d] is the price on day d. Buy on one day and sell on a LATER day.
# Return the biggest profit, or 0 if every trade would lose money.
#
# Every pair:        try each buy day i and each later sell day j. O(n^2).
# Cheapest before:   for each sell day j, the best buy day is the cheapest day
#                    before it: min(prices[:j]). Still O(n^2), hidden in min.
# Carry the cheapest: the cheapest day before j + 1 is the cheaper of "the
#                    cheapest day before j" and day j. Keep it in one name, low.
#                    O(n) time, O(1) memory.
from typing import List


class SolutionPairs:
    def maxProfit(self, prices: List[int]) -> int:
        best = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                best = max(best, prices[j] - prices[i])
        return best


class SolutionMinBefore:
    def maxProfit(self, prices: List[int]) -> int:
        best = 0
        for j in range(1, len(prices)):
            low = min(prices[:j])
            best = max(best, prices[j] - low)
        return best


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        low = prices[0]
        best = 0
        for j in range(1, len(prices)):
            best = max(best, prices[j] - low)
            low = min(low, prices[j])
        return best


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionPairs(), SolutionMinBefore(), Solution())
    for prices, want in (([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0), ([2, 9, 1, 4], 7), ([2, 4, 1], 2), ([5], 0), ([3, 3, 3], 0)):
        assert all(s.maxProfit(prices) == want for s in sols), prices
    for _ in range(5000):
        prices = [random.randint(0, 20) for _ in range(random.randint(1, 12))]
        want = max([0] + [prices[j] - prices[i] for i in range(len(prices)) for j in range(i + 1, len(prices))])
        assert all(s.maxProfit(prices) == want for s in sols), prices
    print("all tests pass")

    for p in ([2, 4, 1], [7, 6, 4, 3, 1]):
        print("max - min on", p, "->", max(p) - min(p), "but the answer is", Solution().maxProfit(p))

    rnd = random.Random(7)
    for n in (2000, 5000, 100000):
        prices = [rnd.randint(0, 10**4) for _ in range(n)]
        for s in sols:
            if n == 100000 and not isinstance(s, Solution):
                continue
            t = time.time(); s.maxProfit(prices); print(f"n = {n}:", type(s).__name__, f"{time.time() - t:.3f}s")
