"""
You are given a 1-indexed integer array nums of length n.

An element nums[i] of nums is called special if i divides n, i.e. n % i == 0.

Return the sum of the squares of all special elements of nums.

EXAMPLE 1:
Input: nums = [1,2,3,4]
Output: 21
Explanation: There are exactly 3 special elements in nums: nums[1] since 1 divides 4, nums[2] since 2 divides 4, and nums[4] since 4 divides 4.
Hence, the sum of the squares of all special elements of nums is nums[1] * nums[1] + nums[2] * nums[2] + nums[4] * nums[4] = 1 * 1 + 2 * 2 + 4 * 4 = 21.

EXAMPLE 2:
Input: nums = [2,7,1,19,18,3]
Output: 63
Explanation: There are exactly 4 special elements in nums: nums[1] since 1 divides 6, nums[2] since 2 divides 6, nums[3] since 3 divides 6, and nums[6] since 6 divides 6.
Hence, the sum of the squares of all special elements of nums is nums[1] * nums[1] + nums[2] * nums[2] + nums[3] * nums[3] + nums[6] * nums[6] = 2 * 2 + 7 * 7 + 1 * 1 + 3 * 3 = 63.

CONSTRAINTS:
- 1 <= nums.length == n <= 50
- 1 <= nums[i] <= 50
"""


class Solution:
    @staticmethod
    def sumOfSquares(nums: list[int]) -> int:
        n = len(nums)
        result = 0
        i = 1

        while i * i <= n:
            if n % i == 0:
                result += nums[i - 1] ** 2

                paired = n // i
                if paired != i:
                    result += nums[paired - 1] ** 2

            i += 1

        return result


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.sumOfSquares([1,2,3,4])
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.sumOfSquares([2,7,1,19,18,3])
    print(f"CASE 2 Result: {result2}")
