# LeetCode 352. Data Stream as Disjoint Intervals (Hard)
#
# Numbers arrive one at a time. When asked, report the numbers seen so far as
# sorted "runs" of consecutive numbers: 1, 2, 3, 6, 7 -> [[1, 3], [6, 7]].
#
# Slow way: remember every number in a set. When asked, sort them and sweep,
#           joining each number to the run before it when it is exactly one more.
#           addNum O(1), getIntervals O(n log n) with n = distinct numbers seen.
# Fast way: keep only the runs, sorted by start. A new number can only touch the
#           run just before it and the run just after it, found by binary search.
#           Five cases: inside, bridge both, join left, join right, stand alone.
#           addNum O(log k) to find + O(k) to insert/remove in a Python list,
#           getIntervals O(k), with k = number of runs (small when merges are common).
from bisect import bisect_right
from typing import List

from sortedcontainers import SortedList


class SummaryRangesSlow:
    def __init__(self):
        self.seen = set()

    def addNum(self, value: int) -> None:
        self.seen.add(value)

    def getIntervals(self) -> List[List[int]]:
        intervals = []
        for v in sorted(self.seen):
            if intervals and intervals[-1][1] == v - 1:
                intervals[-1][1] = v
            else:
                intervals.append([v, v])
        return intervals


class SummaryRanges:
    def __init__(self):
        self.iv = []                     # sorted [start, end] runs that do not touch

    def addNum(self, value: int) -> None:
        i = bisect_right(self.iv, value, key=lambda p: p[0])   # first run starting after value
        left = self.iv[i - 1] if i > 0 else None
        right = self.iv[i] if i < len(self.iv) else None
        if left is not None and left[1] >= value:
            return                       # already inside the left run
        joins_left = left is not None and left[1] == value - 1
        joins_right = right is not None and right[0] == value + 1
        if joins_left and joins_right:   # value bridges the gap: merge both runs
            left[1] = right[1]
            self.iv.pop(i)
        elif joins_left:                 # grow the left run by one at its end
            left[1] = value
        elif joins_right:                # grow the right run by one at its start
            right[0] = value
        else:                            # a new run of its own
            self.iv.insert(i, [value, value])

    def getIntervals(self) -> List[List[int]]:
        return [[s, e] for s, e in self.iv]   # a copy, so later adds cannot change it


class SummaryRangesSortedList:
    """Same five cases, but SortedList makes inserts and removals O(log k)."""

    def __init__(self):
        self.iv = SortedList(key=lambda p: p[0])

    def addNum(self, value: int) -> None:
        i = self.iv.bisect_key_right(value)
        left = self.iv[i - 1] if i > 0 else None
        right = self.iv[i] if i < len(self.iv) else None
        if left is not None and left[1] >= value:
            return
        joins_left = left is not None and left[1] == value - 1
        joins_right = right is not None and right[0] == value + 1
        if joins_left and joins_right:
            left[1] = right[1]
            self.iv.pop(i)
        elif joins_left:
            left[1] = value
        elif joins_right:
            self.iv.pop(i)               # its start (the sort key) changes, so re-add it
            self.iv.add([value, right[1]])
        else:
            self.iv.add([value, value])

    def getIntervals(self) -> List[List[int]]:
        return [[s, e] for s, e in self.iv]


if __name__ == "__main__":
    import random
    import time

    want = [[[1, 1]], [[1, 1], [3, 3]], [[1, 1], [3, 3], [7, 7]], [[1, 3], [7, 7]], [[1, 3], [6, 7]]]
    for cls in (SummaryRangesSlow, SummaryRanges, SummaryRangesSortedList):
        sr = cls()
        got = []
        for v in [1, 3, 7, 2, 6]:
            sr.addNum(v)
            got.append(sr.getIntervals())
        assert got == want, (cls.__name__, got)
    for _ in range(3000):
        objs = [SummaryRangesSlow(), SummaryRanges(), SummaryRangesSortedList()]
        for _ in range(random.randint(1, 40)):
            v = random.randint(0, 25)
            for o in objs:
                o.addNum(v)
            a = objs[0].getIntervals()
            assert objs[1].getIntervals() == a and objs[2].getIntervals() == a
    print("all tests pass")

    # The follow-up: many merges, few runs. 30,000 adds and 100 gets.
    values = [random.randint(0, 10000) for _ in range(29900)]
    for cls in (SummaryRangesSlow, SummaryRanges, SummaryRangesSortedList):
        t = time.time()
        sr = cls()
        for j, v in enumerate(values):
            sr.addNum(v)
            if j % 299 == 0:
                sr.getIntervals()
        print(cls.__name__, f"{time.time() - t:.2f}s")
