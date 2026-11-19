# LeetCode 3413. Maximum Coins From K Consecutive Bags (Medium)
#
# One bag sits at every whole number on a line. coins[i] = [l, r, c] means every
# bag from l to r holds c coins; the segments do not overlap. Take k bags in a
# row; return the most coins you can get.
#
# Slide bag by bag:   lay the bags out and try every start. Needs memory and
#                     time for every position, and positions go up to 10^9.
# Edge candidates:    some best window starts at a segment's left end or ends at
#                     a segment's right end. Try those 2n windows, each against
#                     every segment. O(n^2).
# Two pointers:       sort; for windows starting at each left end, a pointer
#                     adds the segments that fit whole, plus a cut piece of the
#                     next. Mirror the line for windows ending at a right end.
#                     O(n log n).
from typing import List


class SolutionSlide:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        bag = {}
        for l, r, c in coins:
            for x in range(l, r + 1):
                bag[x] = c
        lo = min(l for l, r, c in coins)
        hi = max(r for l, r, c in coins)
        best = 0
        for s in range(lo - k + 1, hi + 1):
            total = 0
            for x in range(s, s + k):
                total += bag.get(x, 0)
            best = max(best, total)
        return best


class SolutionEdges:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        best = 0
        for l, r, c in coins:
            for s in (l, r - k + 1):
                e = s + k - 1
                total = 0
                for a, b, w in coins:
                    lo = max(a, s)
                    hi = min(b, e)
                    if lo <= hi:
                        total += (hi - lo + 1) * w
                best = max(best, total)
        return best


class Solution:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        def slide(segs):
            segs.sort()
            n = len(segs)
            best = full = 0
            j = 0
            for i in range(n):
                e = segs[i][0] + k - 1
                while j < n and segs[j][1] <= e:
                    full += (segs[j][1] - segs[j][0] + 1) * segs[j][2]
                    j += 1
                part = 0
                if j < n and segs[j][0] <= e:
                    part = (e - segs[j][0] + 1) * segs[j][2]
                best = max(best, full + part)
                if j > i:
                    full -= (segs[i][1] - segs[i][0] + 1) * segs[i][2]
                else:
                    j = i + 1
            return best

        left = slide([[l, r, c] for l, r, c in coins])
        right = slide([[-r, -l, c] for l, r, c in coins])
        return max(left, right)


def mistakes():
    def only_left_edges(coins, k):
        # tries only windows that start at a segment's left end
        best = 0
        for l, r, c in coins:
            e = l + k - 1
            best = max(best, sum((min(b, e) - max(a, l) + 1) * w for a, b, w in coins if max(a, l) <= min(b, e)))
        return best

    def whole_segments_only(coins, k):
        # two pointers that forget the cut piece of the next segment
        segs = sorted(coins); n = len(segs); best = full = 0; j = 0
        for i in range(n):
            e = segs[i][0] + k - 1
            while j < n and segs[j][1] <= e:
                full += (segs[j][1] - segs[j][0] + 1) * segs[j][2]; j += 1
            best = max(best, full)
            if j > i:
                full -= (segs[i][1] - segs[i][0] + 1) * segs[i][2]
            else:
                j = i + 1
        return best

    def unsorted(coins, k):
        # same two pointers, but without sorting the segments first
        def slide(segs):
            n = len(segs); best = full = 0; j = 0
            for i in range(n):
                e = segs[i][0] + k - 1
                while j < n and segs[j][1] <= e:
                    full += (segs[j][1] - segs[j][0] + 1) * segs[j][2]; j += 1
                part = (e - segs[j][0] + 1) * segs[j][2] if j < n and segs[j][0] <= e else 0
                best = max(best, full + part)
                if j > i:
                    full -= (segs[i][1] - segs[i][0] + 1) * segs[i][2]
                else:
                    j = i + 1
            return best
        return max(slide([s[:] for s in coins]), slide([[-r, -l, c] for l, r, c in coins]))

    return only_left_edges, whole_segments_only, unsorted


if __name__ == "__main__":
    import random
    import time

    def random_case(max_n, span, max_k):
        n = random.randint(1, max_n); pts = sorted(random.sample(range(1, span + 1), 2 * n))
        coins = [[pts[2 * q], pts[2 * q + 1] - random.randint(0, 1) * (pts[2 * q + 1] > pts[2 * q]), random.randint(1, 9)] for q in range(n)]
        random.shuffle(coins)
        return coins, random.randint(1, max_k)

    for coins, k, want in (([[8, 10, 1], [1, 3, 2], [5, 6, 4]], 4, 10), ([[1, 10, 3]], 2, 6)):
        for s in (SolutionSlide(), SolutionEdges(), Solution()):
            assert s.maximumCoins([c[:] for c in coins], k) == want, (type(s).__name__, coins, k)
    for _ in range(5000):
        coins, k = random_case(5, 30, 15)
        want = SolutionSlide().maximumCoins(coins, k)
        for s in (SolutionEdges(), Solution()):
            assert s.maximumCoins([c[:] for c in coins], k) == want, (type(s).__name__, coins, k)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            coins, k = random_case(3, 10, 6)
            if f([c[:] for c in coins], k) != Solution().maximumCoins([c[:] for c in coins], k):
                if found is None or (len(coins), max(r for l, r, c in coins), k) < (len(found[0]), max(r for l, r, c in found[0]), found[1]):
                    found = (coins, k)
        print(f.__name__, "fails on coins, k =", found, "->", f([c[:] for c in found[0]], found[1]), "instead of", Solution().maximumCoins([c[:] for c in found[0]], found[1])) if found else print(f.__name__, "found no failure")

    rnd = random.Random(7)
    for n in (2000, 10**5):
        pts = sorted(rnd.sample(range(1, 10**9), 2 * n))
        coins = [[pts[2 * q], pts[2 * q + 1], rnd.randint(1, 1000)] for q in range(n)]
        for s in (SolutionEdges(), Solution()):
            if n > 2000 and isinstance(s, SolutionEdges):
                continue
            t0 = time.time(); s.maximumCoins([c[:] for c in coins], 10**7); print(f"n = {n}:", type(s).__name__, f"{time.time() - t0:.3f}s")
    coins = [[1, 100000, 5]]
    t0 = time.time(); SolutionSlide().maximumCoins(coins, 1000); print("one segment of 100000 bags, k = 1000: SolutionSlide", f"{time.time() - t0:.3f}s")
