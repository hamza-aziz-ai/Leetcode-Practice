# LeetCode 2747. Count Zero Request Servers (Medium)
#
# n servers (ids 1..n). logs[i] = [server_id, time]: that server got a request at
# that time. For each query q, count the servers with NO request in the window
# [q - x, q] (both ends included).
#
# Scan every log:   for each query, walk all logs and collect the busy servers
#                   in a set. O(queries * logs).
# Sort and slide:   answers go back by index, so the queries may be handled in
#                   time order. Then the window only moves right: logs enter on
#                   its right edge and leave on its left edge, each once. Keep a
#                   count per server and how many servers have count > 0.
#                   O(L log L + Q log Q + n).
from typing import List


class SolutionScan:
    def countServers(self, n: int, logs: List[List[int]], x: int, queries: List[int]) -> List[int]:
        ans = []
        for q in queries:
            busy = set()
            for server, time in logs:
                if q - x <= time <= q:
                    busy.add(server)
            ans.append(n - len(busy))
        return ans


class Solution:
    def countServers(self, n: int, logs: List[List[int]], x: int, queries: List[int]) -> List[int]:
        logs.sort(key=lambda log: log[1])
        order = sorted(range(len(queries)), key=lambda k: queries[k])
        count = [0] * (n + 1)
        active = 0
        left = right = 0
        ans = [0] * len(queries)
        for k in order:
            q = queries[k]
            while right < len(logs) and logs[right][1] <= q:
                server = logs[right][0]
                count[server] += 1
                if count[server] == 1:
                    active += 1
                right += 1
            while left < right and logs[left][1] < q - x:
                server = logs[left][0]
                count[server] -= 1
                if count[server] == 0:
                    active -= 1
                left += 1
            ans[k] = n - active
        return ans


def mistakes():
    def strict_left(n, logs, x, queries):
        # removing logs with time <= q - x drops a request made exactly at q - x
        logs = sorted(logs, key=lambda l: l[1]); order = sorted(range(len(queries)), key=lambda k: queries[k])
        count = [0] * (n + 1); active = left = right = 0; ans = [0] * len(queries)
        for k in order:
            q = queries[k]
            while right < len(logs) and logs[right][1] <= q:
                count[logs[right][0]] += 1; active += count[logs[right][0]] == 1; right += 1
            while left < right and logs[left][1] <= q - x:
                count[logs[left][0]] -= 1; active -= count[logs[left][0]] == 0; left += 1
            ans[k] = n - active
        return ans

    def unsorted_queries(n, logs, x, queries):
        logs = sorted(logs, key=lambda l: l[1])
        count = [0] * (n + 1); active = left = right = 0; ans = []
        for q in queries:
            while right < len(logs) and logs[right][1] <= q:
                count[logs[right][0]] += 1; active += count[logs[right][0]] == 1; right += 1
            while left < right and logs[left][1] < q - x:
                count[logs[left][0]] -= 1; active -= count[logs[left][0]] == 0; left += 1
            ans.append(n - active)
        return ans

    def count_logs(n, logs, x, queries):
        # counting requests instead of servers: a server with two requests counts twice
        return [n - sum(1 for s, t in logs if q - x <= t <= q) for q in queries]

    print("removing time <= q - x on Example 1 ->", strict_left(3, [[1, 3], [2, 6], [1, 5]], 5, [10, 11]), "instead of [1, 2]")
    print("queries left unsorted on [13, 6, 9] ->", unsorted_queries(4, [[1, 2], [2, 5], [3, 7], [1, 8], [4, 12], [2, 13]], 4, [13, 6, 9]), "instead of [2, 2, 1]")
    print("counting requests, not servers, on n = 2, logs [[1, 3], [1, 4]], x = 5, queries [6] ->", count_logs(2, [[1, 3], [1, 4]], 5, [6]), "instead of [1]")


if __name__ == "__main__":
    import random
    import time

    for args, want in (((3, [[1, 3], [2, 6], [1, 5]], 5, [10, 11]), [1, 2]), ((3, [[2, 4], [2, 1], [1, 2], [3, 1]], 2, [3, 4]), [0, 1]),
                       ((4, [[1, 2], [2, 5], [3, 7], [1, 8], [4, 12], [2, 13]], 4, [13, 6, 9]), [2, 2, 1]), ((2, [[1, 1]], 1, [5]), [2])):
        for s in (SolutionScan(), Solution()):
            n, logs, x, qs = args
            assert s.countServers(n, [l[:] for l in logs], x, qs[:]) == want, (type(s).__name__, args)
    for _ in range(5000):
        n = random.randint(1, 5)
        logs = [[random.randint(1, n), random.randint(1, 20)] for _ in range(random.randint(1, 8))]
        x = random.randint(1, 10)
        qs = [random.randint(x + 1, 25) for _ in range(random.randint(1, 5))]
        want = SolutionScan().countServers(n, [l[:] for l in logs], x, qs[:])
        assert Solution().countServers(n, [l[:] for l in logs], x, qs[:]) == want
    print("all tests pass")
    mistakes()

    rnd = random.Random(5)
    for L in (3000, 10**5):
        n = 10**5
        logs = [[rnd.randint(1, n), rnd.randint(1, 10**6)] for _ in range(L)]
        qs = [rnd.randint(10**5 + 1, 10**6) for _ in range(L)]
        for s in (SolutionScan(), Solution()):
            if L > 3000 and isinstance(s, SolutionScan):
                continue
            t = time.time(); s.countServers(n, [l[:] for l in logs], 10**5, qs[:]); print(f"{L} logs and {L} queries:", type(s).__name__, f"{time.time() - t:.3f}s")
