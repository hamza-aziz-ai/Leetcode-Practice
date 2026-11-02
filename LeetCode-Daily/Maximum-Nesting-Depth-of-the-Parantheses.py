"""
Given a valid parentheses string s, return the nesting depth of s. The nesting depth is the maximum number of nested parentheses.

EXAMPLE 1:
Input: s = "(1+(2*3)+((8)/4))+1"
Output: 3
Explanation: Digit 8 is inside 3 nested parentheses in the string.

EXAMPLE 2:
Input: s = "(1)+((2))+(((3)))"
Output: 3
Explanation: Digit 3 is inside 3 nested parentheses in the string.

EXAMPLEe 3:
Input: s = "()(())((()()))"
Output: 3

CONSTRAINTS:
- 1 <= s.length <= 100
- s consists of digits 0-9 and characters '+', '-', '*', '/', '(', and ')'.
- It is guaranteed that parentheses expression s is a VPS.
"""

class Solution:
    @staticmethod
    def maxDepth(s: str) -> int:
        stack = list()
        depth = list()

        for i, char in enumerate(s):
            if char == "(":
                stack.append(char)
                depth.append(len(stack))
            elif char == ")":
                stack.pop()


        return max(depth) if depth else 0


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.maxDepth("(1+(2*3)+((8)/4))+1")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.maxDepth("(1)+((2))+(((3)))")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.maxDepth("()(())((()()))")
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.maxDepth("1")
    print(f"CASE 4 Result: {result4}")
