# LeetCode 3736. Minimum Moves to Equal Array Elements III (Easy)
# One move adds 1 to a single element. Elements can only grow, so the
# cheapest common value is the current maximum. Every element x needs
# (max - x) moves, which adds up to max * n - sum(nums).
# Time O(n), memory O(1).
from typing import List


class Solution:
    def minMoves(self, nums: List[int]) -> int:
        tallest = max(nums)
        moves = 0
        for i in range(len(nums)):
            x = nums[i]
            need = tallest - x
            moves += need
        return moves

    def minMovesShortcut(self, nums: List[int]) -> int:
        n = len(nums)
        mx = max(nums)
        s = sum(nums)
        box = mx * n
        return box - s


if __name__ == "__main__":
    sol = Solution()
    for nums, want in [([2, 1, 3], 3), ([4, 4, 5], 2), ([3, 3, 3], 0), ([7], 0)]:
        assert sol.minMoves(nums) == want and sol.minMovesShortcut(nums) == want
    print("all tests pass")
