# LeetCode 1882. Process Tasks Using Servers (Medium)
#
# servers[i] is server i's weight; tasks[j] is how long task j takes. Task j
# joins the queue at second j. The front task goes to the free server with the
# smallest weight (ties: smallest index). With no free server, wait until one
# frees up. Return which server got each task.
#
# Scan every server: keep free_at[i] (when server i is free). For each task,
#                    find the start time t, then scan all servers for the best
#                    free one. O(m * n).
# Two heaps:         free servers ordered by (weight, index); busy servers
#                    ordered by (free time, weight, index). Each task does a
#                    few pushes and pops. O((n + m) log n).
from heapq import heapify, heappop, heappush
from typing import List


class SolutionScan:
    def assignTasks(self, servers: List[int], tasks: List[int]) -> List[int]:
        n = len(servers)
        free_at = [0] * n
        ans = []
        t = 0
        for j, d in enumerate(tasks):
            t = max(t, j)
            if min(free_at) > t:
                t = min(free_at)
            best = -1
            for i in range(n):
                if free_at[i] <= t and (best == -1 or servers[i] < servers[best]):
                    best = i
            free_at[best] = t + d
            ans.append(best)
        return ans


class Solution:
    def assignTasks(self, servers: List[int], tasks: List[int]) -> List[int]:
        free = [(w, i) for i, w in enumerate(servers)]
        heapify(free)
        busy = []
        ans = []
        t = 0
        for j, d in enumerate(tasks):
            t = max(t, j)
            if not free:
                t = max(t, busy[0][0])
            while busy and busy[0][0] <= t:
                _, w, i = heappop(busy)
                heappush(free, (w, i))
            w, i = heappop(free)
            heappush(busy, (t + d, w, i))
            ans.append(i)
        return ans


def mistakes():
    def start_at_j(servers, tasks):
        # forgets that tasks wait in the queue: start time is always j
        free = [(w, i) for i, w in enumerate(servers)]; heapify(free); busy = []; ans = []
        for j, d in enumerate(tasks):
            t = j
            if not free:
                t = max(t, busy[0][0])
            while busy and busy[0][0] <= t:
                _, w, i = heappop(busy); heappush(free, (w, i))
            w, i = heappop(free); heappush(busy, (t + d, w, i)); ans.append(i)
        return ans

    def pop_one_no_weight(servers, tasks):
        # busy keyed by (free time, index) only, and when nobody is free it frees just
        # ONE server: if two free up at the same second, the lighter one can be missed
        free = [(w, i) for i, w in enumerate(servers)]; heapify(free); busy = []; ans = []; t = 0
        for j, d in enumerate(tasks):
            t = max(t, j)
            while busy and busy[0][0] <= t:
                _, i = heappop(busy); heappush(free, (servers[i], i))
            if not free:
                ft, i = heappop(busy); t = ft; heappush(free, (servers[i], i))
            w, i = heappop(free); heappush(busy, (t + d, i)); ans.append(i)
        return ans

    return start_at_j, pop_one_no_weight


if __name__ == "__main__":
    import random
    import time

    for servers, tasks, want in (([3, 3, 2], [1, 2, 3, 2, 1, 2], [2, 2, 0, 2, 1, 2]), ([5, 1, 4, 3, 2], [2, 1, 2, 4, 5, 2, 1], [1, 4, 1, 4, 1, 3, 2])):
        assert SolutionScan().assignTasks(servers, tasks) == want and Solution().assignTasks(servers, tasks) == want
    for _ in range(5000):
        servers = [random.randint(1, 4) for _ in range(random.randint(1, 5))]
        tasks = [random.randint(1, 6) for _ in range(random.randint(1, 9))]
        assert Solution().assignTasks(servers, tasks) == SolutionScan().assignTasks(servers, tasks), (servers, tasks)
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            servers = [random.randint(1, 4) for _ in range(random.randint(1, 3))]
            tasks = [random.randint(1, 4) for _ in range(random.randint(1, 6))]
            if f(servers, tasks) != SolutionScan().assignTasks(servers, tasks):
                if found is None or len(servers) + len(tasks) < len(found[0]) + len(found[1]):
                    found = (servers, tasks)
        if found:
            print(f.__name__, "fails on servers =", found[0], "tasks =", found[1], "->", f(*found), "instead of", SolutionScan().assignTasks(*found))
        else:
            print(f.__name__, "found no failure")

    rnd = random.Random(2)
    for n, m in ((3000, 3000), (2 * 10**5, 2 * 10**5)):
        servers = [rnd.randint(1, 2 * 10**5) for _ in range(n)]
        tasks = [rnd.randint(1, 2 * 10**5) for _ in range(m)]
        for s in (SolutionScan(), Solution()):
            if n > 3000 and isinstance(s, SolutionScan):
                continue
            t0 = time.time(); s.assignTasks(servers, tasks); print(f"n = m = {n}:", type(s).__name__, f"{time.time() - t0:.3f}s")
