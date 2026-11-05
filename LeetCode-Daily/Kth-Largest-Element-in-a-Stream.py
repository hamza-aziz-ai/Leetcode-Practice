# LeetCode 703. Kth Largest Element in a Stream (Easy)
#
# Story: scores arrive one by one. Only the k best scores get an interview.
# After each new score, report the cut-off: the lowest score that still gets
# an interview, which is the kth largest score so far.
#
# Slow way: keep every score, sort them all on each add.
#           add: O(n log n) (Timsort is close to O(n) here, since the list is
#           already sorted except one item), memory O(n) and growing.
# Fast way: keep only the k best scores in a min-heap. The smallest of them,
#           heap[0], is the cut-off.  add: O(log k), memory O(k).
import heapq
from typing import List


class KthLargestSlow:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.nums = list(nums)

    def add(self, val: int) -> int:
        self.nums.append(val)
        self.nums.sort(reverse=True)
        return self.nums[self.k - 1]


class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


# Textbook versions of push and pop, used by the explainer page. Python's own
# heapq moves items instead of swapping pairs, and its pop first walks down to
# a leaf, but the list of values it ends with is the same. Checked below.
def push_textbook(heap, val):
    heap.append(val)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[i] < heap[parent]:
            heap[i], heap[parent] = heap[parent], heap[i]
            i = parent
        else:
            break


def pop_textbook(heap):
    smallest = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i = 0
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            child = left
            if right < len(heap) and heap[right] <= heap[left]:
                child = right               # on a tie Python takes the right child
            if child < len(heap) and heap[child] < heap[i]:
                heap[i], heap[child] = heap[child], heap[i]
                i = child
            else:
                break
    return smallest


if __name__ == "__main__":
    import random

    def run(cls, k, nums, adds):
        obj = cls(k, nums)
        return [obj.add(v) for v in adds]

    assert run(KthLargest, 3, [4, 5, 8, 2], [3, 5, 10, 9, 4]) == [4, 5, 5, 8, 8]
    assert run(KthLargest, 4, [7, 7, 7, 7, 8, 3], [2, 10, 9, 9]) == [7, 7, 7, 8]
    assert run(KthLargest, 1, [], [-3, -2, -4, 0, 4]) == [-3, -2, -2, 0, 4]
    for _ in range(3000):
        nums = [random.randint(-9, 9) for _ in range(random.randint(0, 10))]
        k = random.randint(1, len(nums) + 1)
        adds = [random.randint(-9, 9) for _ in range(random.randint(1, 10))]
        assert run(KthLargest, k, nums, adds) == run(KthLargestSlow, k, nums, adds)
    for _ in range(3000):
        a, b = [], []
        for _ in range(random.randint(1, 30)):
            v = random.randint(-5, 5)
            heapq.heappush(a, v)
            push_textbook(b, v)
            assert a == b
            if random.random() < 0.4 and a:
                assert heapq.heappop(a) == pop_textbook(b)
                assert a == b
    print("all tests pass")
