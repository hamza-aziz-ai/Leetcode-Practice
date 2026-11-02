"""
Design and implement a data structure for a Least Frequently Used (LFU) cache.

Implement the LFUCache class:
- LFUCache(int capacity) Initializes the object with the capacity of the data structure.
- int get(int key) Gets the value of the key if the key exists in the cache. Otherwise, returns -1.
- void put(int key, int value) Update the value of the key if present, or inserts the key if not already present
  When the cache reaches its capacity, it should invalidate and remove the least frequently used key before inserting a new item.
  For this problem, when there is a tie (i.e., two or more keys with the same frequency), the least recently used key would be invalidated.
  To determine the least frequently used key, a use counter is maintained for each key in the cache. The key with the smallest use counter is the least frequently used key.

When a key is first inserted into the cache, its use counter is set to 1 (due to the put operation).
The use counter for a key in the cache is incremented either a get or put operation is called on it.

The functions get and put must each run in O(1) average time complexity.

EXAMPLE 1:
Input
["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, 3, null, -1, 3, 4]

Explanation
// cnt(x) = the use counter for key x
// cache=[] will show the last used order for tiebreakers (leftmost element is  most recent)
LFUCache lfu = new LFUCache(2);
lfu.put(1, 1);   // cache=[1,_], cnt(1)=1
lfu.put(2, 2);   // cache=[2,1], cnt(2)=1, cnt(1)=1
lfu.get(1);      // return 1
                 // cache=[1,2], cnt(2)=1, cnt(1)=2
lfu.put(3, 3);   // 2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
                 // cache=[3,1], cnt(3)=1, cnt(1)=2
lfu.get(2);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,1], cnt(3)=2, cnt(1)=2
lfu.put(4, 4);   // Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
                 // cache=[4,3], cnt(4)=1, cnt(3)=2
lfu.get(1);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,4], cnt(4)=1, cnt(3)=3
lfu.get(4);      // return 4
                 // cache=[4,3], cnt(4)=2, cnt(3)=3

CONSTRAINTS:
- 1 <= capacity <= 104
- 0 <= key <= 105
- 0 <= value <= 109
- At most 2 * 105 calls will be made to get and put.
"""
from collections import OrderedDict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, tuple[int, int]] = {}
        self.buckets: dict[int, OrderedDict[int, None]] = {}
        self.min_frequency = 0
        print("======================================================================================================")
        print(f"INITIALIZATION")
        print("======================================================================================================")
        print(f"Initial Capacity: {self.capacity}")
        print(f"Initial LFU Cache: {self.cache}")
        print(f"Initial Frequency Buckets: {self.buckets}")
        print(f"Initial Minimum Frequency: {self.min_frequency}")
        print("======================================================================================================\n")

    def _touch(self, key: int) -> None:
        value, frequency = self.cache[key]

        # Move the key from frequency f to frequency f + 1.
        bucket = self.buckets[frequency]
        del bucket[key]

        if not bucket:
            del self.buckets[frequency]
            if self.min_frequency == frequency:
                self.min_frequency += 1

        frequency += 1
        self.cache[key] = (value, frequency)
        self.buckets.setdefault(frequency, OrderedDict())[key] = None

        print("--------------------------------------------------------------------------------------------------")
        print(f"Bucket Update: {self.buckets}")
        print("--------------------------------------------------------------------------------------------------\n")

    def get(self, key: int) -> int:
        print("======================================================================================================")
        print(f"After GET Operation Performed")
        print("======================================================================================================")
        print(f"Key to get value: {key}")

        if key not in self.cache:
            print(f"Key {key} does not exist, returning {-1}")
            print("======================================================================================================\n")
            return -1

        value, _ = self.cache[key]
        self._touch(key)

        print(f"Value of {key}: {value}")
        print("======================================================================================================\n")

        return value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            print("--------------------------------------------------------------------------------------------------")
            print(f"Capacity is {self.capacity}")
            print("--------------------------------------------------------------------------------------------------\n")
            return

        if key in self.cache:
            print("--------------------------------------------------------------------------------------------------")
            print(f"Key {key} already present in {self.cache}")
            print("--------------------------------------------------------------------------------------------------\n")
            _, frequency = self.cache[key]
            self.cache[key] = (value, frequency)
            self._touch(key)
            return

        if len(self.cache) == self.capacity:
            print("--------------------------------------------------------------------------------------------------")
            print(f"Length has {len(self.cache)}")
            print("--------------------------------------------------------------------------------------------------\n")
            bucket = self.buckets[self.min_frequency]
            oldest, _ = bucket.popitem(last=False)
            del self.cache[oldest]

            if not bucket:
                del self.buckets[self.min_frequency]

        self.cache[key] = (value, 1)
        self.buckets.setdefault(1, OrderedDict())[key] = None
        self.min_frequency = 1

        print("======================================================================================================")
        print(f"After PUT Operation Performed")
        print("======================================================================================================")
        print(f"Capacity: {self.capacity}")
        print(f"LFU Cache: {self.cache}")
        print(f"Frequency Buckets: {self.buckets}")
        print(f"Minimum Frequency: {self.min_frequency}")
        print("======================================================================================================\n")


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)


if __name__ == "__main__":
    lfu = LFUCache(3)
    lfu.put(2, 2)
    lfu.put(1, 1)
    lfu.get(2)
    lfu.get(1)
    lfu.get(2)
    lfu.put(3, 3)
    lfu.put(4, 4)
    lfu.get(3)
    lfu.get(2)
    lfu.get(1)
    lfu.get(4)

    print()

    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    lfu.get(1)
    lfu.put(3, 3)
    lfu.get(2)
    lfu.get(3)
    lfu.put(4, 4)
    lfu.get(1)
    lfu.get(3)
    lfu.get(4)
