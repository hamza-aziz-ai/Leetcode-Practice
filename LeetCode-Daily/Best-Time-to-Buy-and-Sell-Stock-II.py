# LeetCode 122. Best Time to Buy and Sell Stock II (Medium)
#
# Buy and sell as many times as you like, holding at most one share at a time
# (buying and selling on the same day is allowed). Return the biggest total profit.
#
# Every plan:       each day, act or wait. 2^n plans. Correct but hopeless.
# Valleys and peaks: walk down to a valley, buy; walk up to a peak, sell. O(n).
# Every climb:      a climb from a valley to a peak is the sum of its daily
#                   steps up, so just add every day that is higher than the day
#                   before. O(n), the simplest code.
# Cash and hold:    two numbers per day: the most money with no share (cash)
#                   and with one share (hold). O(n), and it still works when the
#                   rules change (a fee, a cooldown, a limit on trades).
from typing import List


class SolutionEveryPlan:
    def maxProfit(self, prices: List[int]) -> int:
        def best(day, holding):
            if day == len(prices):
                return 0
            wait = best(day + 1, holding)
            if holding:
                act = prices[day] + best(day + 1, False)
            else:
                act = -prices[day] + best(day + 1, True)
            return max(wait, act)
        return best(0, False)


class SolutionValleyPeak:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        profit = 0
        i = 0
        while i < n - 1:
            while i < n - 1 and prices[i + 1] <= prices[i]:
                i += 1
            valley = prices[i]
            while i < n - 1 and prices[i + 1] >= prices[i]:
                i += 1
            peak = prices[i]
            profit += peak - valley
        return profit


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0
        for j in range(1, len(prices)):
            if prices[j] > prices[j - 1]:
                profit += prices[j] - prices[j - 1]
        return profit


class SolutionCashHold:
    def maxProfit(self, prices: List[int]) -> int:
        cash = 0
        hold = -prices[0]
        for j in range(1, len(prices)):
            new_cash = max(cash, hold + prices[j])
            new_hold = max(hold, cash - prices[j])
            cash, hold = new_cash, new_hold
        return cash


def strict_valley_peak(prices, cap=1000):
    """The mistake: strict < and > in both inner loops. Returns None if it never finishes."""
    n, profit, i, steps = len(prices), 0, 0, 0
    while i < n - 1:
        steps += 1
        if steps > cap:
            return None
        while i < n - 1 and prices[i + 1] < prices[i]:
            i += 1
        valley = prices[i]
        while i < n - 1 and prices[i + 1] > prices[i]:
            i += 1
        profit += prices[i] - valley
    return profit


if __name__ == "__main__":
    import random
    import time

    sols = (SolutionEveryPlan(), SolutionValleyPeak(), Solution(), SolutionCashHold())
    for prices, want in (([7, 1, 5, 3, 6, 4], 7), ([1, 2, 3, 4, 5], 4), ([7, 6, 4, 3, 1], 0), ([3, 3, 5, 5, 2, 4], 4), ([5], 0), ([3, 3], 0)):
        assert all(s.maxProfit(prices) == want for s in sols), prices
    for _ in range(5000):
        prices = [random.randint(0, 9) for _ in range(random.randint(1, 11))]
        want = SolutionEveryPlan().maxProfit(prices)
        assert all(s.maxProfit(prices) == want for s in sols), prices
    print("all tests pass")

    print("one trade only (LeetCode 121) on [7, 1, 5, 3, 6, 4] -> 5 instead of 7")
    print("strict < and > on [3, 3] ->", strict_valley_peak([3, 3]), "(None: the outer loop never moves)")
    c, h = 0, 0
    for p in [5, 7][1:]:
        c, h = max(c, h + p), max(h, c - p)
    print("hold = 0 at the start on [5, 7] ->", c, "instead of 2")

    rnd = random.Random(3)
    for n in (16, 18, 20):
        prices = [rnd.randint(0, 10**4) for _ in range(n)]
        t = time.time(); SolutionEveryPlan().maxProfit(prices); print(f"n = {n}: SolutionEveryPlan {time.time() - t:.3f}s")
    prices = [rnd.randint(0, 10**4) for _ in range(30000)]
    for s in sols[1:]:
        t = time.time(); s.maxProfit(prices); print("n = 30000:", type(s).__name__, f"{time.time() - t:.4f}s")
