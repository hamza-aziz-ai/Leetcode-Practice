"""
Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses substring.

EXAMPLE 1:
Input: s = "(()"
Output: 2
Explanation: The longest valid parentheses substring is "()".

EXAMPLE 2:
Input: s = ")()())"
Output: 4
Explanation: The longest valid parentheses substring is "()()".

EXAMPLE 3:
Input: s = ""
Output: 0

CONSTRAINTS:
- 0 <= s.length <= 3 * 104
- s[i] is '(', or ')'.
"""

class Solution:
    @staticmethod
    def longestValidParentheses(s: str) -> int:
        valid_parentheses_list = [" "] * len(s)
        stack = list()
        index_stack = list()

        for i, char in enumerate(s):
            if char == ")" and stack and stack[-1] == "(":
                valid_parentheses_list[index_stack[-1]], valid_parentheses_list[i] = stack[-1], char
                stack.pop()
                index_stack.pop()
            else:
                stack.append(char)
                index_stack.append(i)

        valid_parentheses_list = "".join(valid_parentheses_list).split(" ")

        return max([len(valid_parentheses) for valid_parentheses in valid_parentheses_list])


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.longestValidParentheses("))())(()))()(((()())(()(((()))))((()(())()((((()))())))())))()(()(()))))())(((())(()()))((())()())((()))(()(())(())((())((((()())()))((()(())()))()(()))))))()))(()))))()())()())()()()()()()()))()(((()()((()(())((()())))(()())))))))(()()(())())(()))))))()()())((((()()()())))))((())(())()()(()((()()))()()())(()())()))()(()(()())))))())()(())(()))(())()(())()((())()((((()()))())(((((())))())())(()((())((()()((((((())))(((())))))))(()()((((((()(((())()(()))(()())((()(((()((()(())())()())(((()))()(((()))))(())))(())()())()(((()))))((())())))())()()))((((()))(())()())()(((())(())(()()((())()())()()())())))((()())(()((()()()(()())(()))(()())((((()(()(((()(((())()((()(()))())()())))))))))))()())()(()(((())()))(((()))((((()())())(()())((()())(()()((()((((()())))()(())(())()))))(())())))))(((((((())(((((()))()))(()()()()))))))(()(()(()(()()(((()()))((()))())((())())()())()))()()(((())))()(())()()(())))(((()))))))))(())((()((()((()))))()()()((())((((((((((()(())))(())((()(()())())(((((((()()()()))())(((()())()(()()))))(()()))))(((()()((()()()(((()))))(()()())()()()(()))))()(())))))))()((((((((()((())))))))(()))()((()())())(")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.longestValidParentheses(")()())")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.longestValidParentheses("")
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.longestValidParentheses("(()")
    print(f"CASE 4 Result: {result4}")
