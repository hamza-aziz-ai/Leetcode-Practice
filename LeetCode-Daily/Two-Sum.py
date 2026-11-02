"""
You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

EXAMPLE 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

EXAMPLE 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

EXAMPLE 3:
Input: nums = [3,3], target = 6
Output: [0,1]

CONSTRAINTS:
* 2 <= nums.length <= 104
* -10^9 <= nums[i] <= 10^9
* -10^9 <= target <= 10^9
* Only one valid answer exists.
"""


class Solution:
    @staticmethod
    def twoSum(nums: list[int], target: int) -> list[int]:
        seen = dict()

        for i, number in enumerate(nums):
            needed = target - number

            if needed in seen:
                return [seen[needed], i]

            seen[number] = i

        # for i in range(len(nums)):
        #     needed = target - nums[i]
        #     print(nums[i], needed)
        #     if needed not in nums:
        #         print("Moving to next item")
        #         continue
        #     first_index = nums.index(needed)
        #     print(f"First occurrence: {first_index}")
        #     if i == first_index:
        #         print(f"First occurrence of {needed} is same as {i}")
        #         try:
        #             next_index = nums.index(needed, first_index + 1)
        #             print(f"Next occurrence of {needed} is {next_index}")
        #             return [i, next_index]
        #         except ValueError:
        #             continue
        #     return [i, first_index]

        # for i in range(len(nums)):
        #     if i == len(nums) - 1:
        #         break
        #     for j in range(i + 1, len(nums)):
        #         if nums[i] + nums[j] == target:
        #             return [i, j]

        return []


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.twoSum([2,7,11,15], 9)
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.twoSum([3,2,4], 6)
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.twoSum([3,3], 6)
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.twoSum([3,2,3], 6)
    print(f"CASE 4 Result: {result4}")

    # Printing blank line seperator
    print()

    # CASE 5
    result5 = solution.twoSum([2,5,5,11], 10)
    print(f"CASE 5 Result: {result5}")
