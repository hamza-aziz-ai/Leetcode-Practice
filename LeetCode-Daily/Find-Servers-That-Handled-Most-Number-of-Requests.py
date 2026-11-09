# LeetCode 1606. Find Servers That Handled Most Number of Requests (Hard)
#
# k servers sit in a circle. Request i arrives at arrival[i] and takes load[i].
# It tries server i % k, then the next ones around the circle; the first free
# server takes it. If every server is busy, the request is dropped. Return the
# servers that handled the most requests.
#
# Walk the circle:      keep free_at[s]; for each request walk up to k servers
#                       starting at i % k. O(n * k).
# Busy heap + free set: busy servers in a heap by (end time, id); free servers
#                       in a sorted list. Find the first free id >= i % k with
#                       a binary search, or wrap to the smallest. O(n log k).
# Heap trick:           no sorted list: keep free servers in a heap keyed so the
#                       smallest key is the next server around the circle.
from heapq import heappop, heappush
from typing import List

from sortedcontainers import SortedList


class SolutionWalk:
    def busiestServers(self, k: int, arrival: List[int], load: List[int]) -> List[int]:
        free_at = [0] * k
        cnt = [0] * k
        for i, (a, d) in enumerate(zip(arrival, load)):
            for step in range(k):
                s = (i + step) % k
                if free_at[s] <= a:
                    free_at[s] = a + d
                    cnt[s] += 1
                    break
        best = max(cnt)
        return [s for s in range(k) if cnt[s] == best]


class Solution:
    def busiestServers(self, k: int, arrival: List[int], load: List[int]) -> List[int]:
        free = SortedList(range(k))
        busy = []
        cnt = [0] * k
        for i, (a, d) in enumerate(zip(arrival, load)):
            while busy and busy[0][0] <= a:
                _, s = heappop(busy)
                free.add(s)
            if not free:
                continue
            p = free.bisect_left(i % k)
            if p == len(free):
                p = 0
            s = free.pop(p)
            heappush(busy, (a + d, s))
            cnt[s] += 1
        best = max(cnt)
        return [s for s in range(k) if cnt[s] == best]


class SolutionHeapTrick:
    # A free server s is stored with key = i + (s - i) % k, the request number at
    # which the walk from i % k would reach it. Keys of servers that sat free
    # while i moved on are refreshed lazily when they come back from busy.
    def busiestServers(self, k: int, arrival: List[int], load: List[int]) -> List[int]:
        free = list(range(k))
        busy = []
        cnt = [0] * k
        for i, (a, d) in enumerate(zip(arrival, load)):
            while busy and busy[0][0] <= a:
                _, s = heappop(busy)
                heappush(free, i + (s - i) % k)
            while free and free[0] < i:
                s = heappop(free) % k
                heappush(free, i + (s - i) % k)
            if not free:
                continue
            s = heappop(free) % k
            heappush(busy, (a + d, s))
            cnt[s] += 1
        best = max(cnt)
        return [s for s in range(k) if cnt[s] == best]


def mistakes():
    def free_only_if_before(k, arrival, load):
        # a server whose request ends exactly when the next one arrives is free
        free = SortedList(range(k)); busy = []; cnt = [0] * k
        for i, (a, d) in enumerate(zip(arrival, load)):
            while busy and busy[0][0] < a:
                free.add(heappop(busy)[1])
            if not free:
                continue
            p = free.bisect_left(i % k)
            s = free.pop(p if p < len(free) else 0); heappush(busy, (a + d, s)); cnt[s] += 1
        best = max(cnt); return [s for s in range(k) if cnt[s] == best]

    def start_at_zero(k, arrival, load):
        # takes the smallest free id, forgetting to start at i % k
        free = SortedList(range(k)); busy = []; cnt = [0] * k
        for i, (a, d) in enumerate(zip(arrival, load)):
            while busy and busy[0][0] <= a:
                free.add(heappop(busy)[1])
            if not free:
                continue
            s = free.pop(0); heappush(busy, (a + d, s)); cnt[s] += 1
        best = max(cnt); return [s for s in range(k) if cnt[s] == best]

    def one_winner(k, arrival, load):
        # returns only one busiest server; ties must all be returned
        cnt = [0] * k; free_at = [0] * k
        for i, (a, d) in enumerate(zip(arrival, load)):
            for step in range(k):
                s = (i + step) % k
                if free_at[s] <= a:
                    free_at[s] = a + d; cnt[s] += 1; break
        return [cnt.index(max(cnt))]

    return free_only_if_before, start_at_zero, one_winner


if __name__ == "__main__":
    import random
    import time

    for k, arrival, load, want in ((3, [1, 2, 3, 4, 5], [5, 2, 3, 3, 3], [1]), (3, [1, 2, 3, 4], [1, 2, 1, 2], [0]), (3, [1, 2, 3], [10, 12, 11], [0, 1, 2])):
        for s in (SolutionWalk(), Solution(), SolutionHeapTrick()):
            assert sorted(s.busiestServers(k, arrival, load)) == want, (type(s).__name__, k, arrival, load)
    for _ in range(5000):
        k = random.randint(1, 5); n = random.randint(1, 10)
        arrival = sorted(random.sample(range(1, 25), n)); load = [random.randint(1, 8) for _ in range(n)]
        want = SolutionWalk().busiestServers(k, arrival, load)
        assert Solution().busiestServers(k, arrival, load) == want and sorted(SolutionHeapTrick().busiestServers(k, arrival, load)) == want, (k, arrival, load)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            k = random.randint(1, 3); n = random.randint(1, 5)
            arrival = sorted(random.sample(range(1, 10), n)); load = [random.randint(1, 4) for _ in range(n)]
            if sorted(f(k, arrival, load)) != Solution().busiestServers(k, arrival, load):
                if found is None or (k + n, sum(load)) < (found[0] + len(found[1]), sum(found[2])):
                    found = (k, arrival, load)
        print(f.__name__, "fails on k, arrival, load =", found, "->", f(*found), "instead of", Solution().busiestServers(*found)) if found else print(f.__name__, "found no failure")

    rnd = random.Random(3)
    for k, n in ((2000, 2000), (10**5, 10**5)):
        arrival = sorted(rnd.sample(range(1, 10**9), n)); load = [rnd.randint(1, 10**9) for _ in range(n)]
        for s in (SolutionWalk(), Solution(), SolutionHeapTrick()):
            if n > 2000 and isinstance(s, SolutionWalk):
                continue
            t0 = time.time(); s.busiestServers(k, arrival, load); print(f"k = n = {n}:", type(s).__name__, f"{time.time() - t0:.3f}s")
    # worst case for the walk: every load is long, so once the servers fill up,
    # each later request walks the whole circle and is dropped
    k = 3000; n = 2 * k; arrival = list(range(1, n + 1)); load = [10**9] * n
    for s in (SolutionWalk(), Solution()):
        t0 = time.time(); s.busiestServers(k, arrival, load); print("all busy, k = 3000, n = 6000:", type(s).__name__, f"{time.time() - t0:.3f}s")
