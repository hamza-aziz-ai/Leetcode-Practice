"""
You are given a string s that consists of lower case English letters and brackets.
Reverse the strings in each pair of matching parentheses, starting from the innermost one.
Your result should not contain any brackets.

EXAMPLE 1:
Input: s = "(abcd)"
Output: "dcba"

Example 2:
Input: s = "(u(love)i)"
Output: "iloveu"
Explanation: The substring "love" is reversed first, then the whole string is reversed.

EXAMPLE 3:
Input: s = "(ed(et(oc))el)"
Output: "leetcode"
Explanation: First, we reverse the substring "oc", then "etco", and finally, the whole string.


CONSTRAINTS:
1 <= s.length <= 2000
s only contains lower case English characters and parentheses.
It is guaranteed that all parentheses are balanced.
"""

# class Solution:
#     def reverseParentheses(self, s: str) -> str:
#         opening_brace_index = 0
#
#         for i, element in enumerate(s):
#             if element == "(":
#                 # Keep track of the latest opening brace
#                 opening_brace_index = i
#
#             elif element == ")":
#                 closing_brace_index = i
#
#                 # Reverse substring between the parentheses
#                 substring = s[opening_brace_index + 1:closing_brace_index]
#                 reversed_substring = substring[::-1]
#
#                 # Remove the parentheses and insert reversed substring
#                 reversed_string = (
#                     s[:opening_brace_index]
#                     + reversed_substring
#                     + s[closing_brace_index + 1:]
#                 )
#
#                 return self.reverseParentheses(reversed_string)
#
#         # Base case: no ')' found
#         return s

class Solution:
    @staticmethod
    def reverseParentheses(s: str) -> str:
        n = len(s)

        stack = []
        pair = [0] * n

        # Pass 1: Match parentheses
        for i, char in enumerate(s):
            if char == "(":
                stack.append(i)

            elif char == ")":
                opening_index = stack.pop()

                pair[opening_index] = i
                pair[i] = opening_index

        # Pass 2: Traverse while changing direction
        result = []

        i = 0
        direction = 1

        while 0 <= i < n:

            if s[i] == "(" or s[i] == ")":
                # Jump to matching parenthesis
                i = pair[i]

                # Reverse direction
                direction *= -1

            else:
                result.append(s[i])

            i += direction

        return "".join(result)


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.reverseParentheses("(abcd)")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.reverseParentheses("(u(love)i)")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.reverseParentheses("(ed(et(oc))el)")
    print(f"CASE 3 Result: {result3}")
