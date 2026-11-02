"""
Write a function to find the longest common prefix string among the input strings.
If there is no common prefix, return an empty string "".

EXAMPLE 1:
Input: strs = ["flower","flow","flight"]
Output: "fl"

EXAMPLE 2:
Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.


CONSTRAINTS:
1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] consists of only lowercase English letters if it is non-empty.
"""

class Solution:
    @staticmethod
    def longestCommonPrefix(strs: list[str]) -> str:
        longest_common_prefix = strs[0]
        intersection = ""
        if len(strs) >= 1:
            for next_element in strs[1:]:
                for letter_a, letter_b in zip(longest_common_prefix, next_element):
                    if letter_a == letter_b:
                        intersection = intersection + letter_a
                    else:
                        break
                longest_common_prefix = intersection
                if intersection == "":
                    break
                intersection = ""

        return longest_common_prefix


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.longestCommonPrefix(strs = ["flower","flow","flight"])
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.longestCommonPrefix(strs = ["dog","racecar","car"])
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result2 = solution.longestCommonPrefix(strs=["cir", "car"])
    print(f"CASE 3 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 4
    result2 = solution.longestCommonPrefix(strs=["racecar", "dog", "race"])
    print(f"CASE 4 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 4
    result2 = solution.longestCommonPrefix(strs=["racecar"])
    print(f"CASE 5 Result: {result2}")
