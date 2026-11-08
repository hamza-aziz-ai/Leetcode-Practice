# LeetCode 1267. Count Servers that Communicate (Medium)
#
# grid[i][j] == 1 means a server sits at row i, column j. Two servers talk if
# they share a row or a column. Count the servers that talk to at least one
# other server.
#
# Look around every server: for each server, walk its whole row and its whole
#                           column looking for another server. O(m * n * (m + n)).
# Count first:              count the servers in every row and every column
#                           once; a server talks if its row or its column holds
#                           more than one server. O(m * n).
from typing import List


class SolutionLook:
    def countServers(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    talks = False
                    for k in range(n):
                        if k != j and grid[i][k] == 1:
                            talks = True
                    for k in range(m):
                        if k != i and grid[k][j] == 1:
                            talks = True
                    if talks:
                        ans += 1
        return ans


class Solution:
    def countServers(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        rows = [0] * m
        cols = [0] * n
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    rows[i] += 1
                    cols[j] += 1
        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and (rows[i] > 1 or cols[j] > 1):
                    ans += 1
        return ans


class SolutionLonely:
    # Same counts, read the other way: every server talks except the lonely
    # ones, which are alone in both their row and their column.
    def countServers(self, grid: List[List[int]]) -> int:
        rows = [sum(r) for r in grid]
        cols = [sum(c) for c in zip(*grid)]
        lonely = sum(1 for i, r in enumerate(grid) for j, v in enumerate(r) if v and rows[i] == 1 and cols[j] == 1)
        return sum(rows) - lonely


def mistakes():
    def and_instead_of_or(grid):
        # needs a partner in the row AND in the column; one partner is enough
        rows = [sum(r) for r in grid]; cols = [sum(c) for c in zip(*grid)]
        return sum(1 for i, r in enumerate(grid) for j, v in enumerate(r) if v and rows[i] > 1 and cols[j] > 1)

    def count_pairs(grid):
        # adds the row and column counts instead of counting each server once
        rows = [sum(r) for r in grid]; cols = [sum(c) for c in zip(*grid)]
        return sum(r for r in rows if r > 1) + sum(c for c in cols if c > 1)

    def greater_than_zero(grid):
        # a row count of 1 is the server itself, not a partner
        rows = [sum(r) for r in grid]; cols = [sum(c) for c in zip(*grid)]
        return sum(1 for i, r in enumerate(grid) for j, v in enumerate(r) if v and (rows[i] > 0 or cols[j] > 0))

    return and_instead_of_or, count_pairs, greater_than_zero


if __name__ == "__main__":
    import random
    import time

    for grid, want in (([[1, 0], [0, 1]], 0), ([[1, 0], [1, 1]], 3), ([[1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]], 4)):
        for s in (SolutionLook(), Solution(), SolutionLonely()):
            assert s.countServers(grid) == want, (type(s).__name__, grid)
    for _ in range(5000):
        m, n = random.randint(1, 5), random.randint(1, 5)
        grid = [[int(random.random() < 0.35) for _ in range(n)] for _ in range(m)]
        want = SolutionLook().countServers(grid)
        assert Solution().countServers(grid) == want and SolutionLonely().countServers(grid) == want, grid
    print("all tests pass")

    for f in mistakes():
        found = None
        for _ in range(20000):
            m, n = random.randint(1, 3), random.randint(1, 3)
            grid = [[int(random.random() < 0.5) for _ in range(n)] for _ in range(m)]
            if f(grid) != Solution().countServers(grid):
                if found is None or len(grid) * len(grid[0]) < len(found) * len(found[0]):
                    found = grid
        print(f.__name__, "fails on", found, "->", f(found), "instead of", Solution().countServers(found)) if found else print(f.__name__, "found no failure")

    rnd = random.Random(1)
    grid = [[int(rnd.random() < 0.5) for _ in range(250)] for _ in range(250)]
    for s in (SolutionLook(), Solution(), SolutionLonely()):
        t0 = time.time(); s.countServers(grid); print("250 x 250:", type(s).__name__, f"{time.time() - t0:.3f}s")
