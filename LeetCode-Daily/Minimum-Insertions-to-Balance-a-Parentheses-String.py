"""
Given a parentheses string s containing only the characters '(' and ')'. A parentheses string is balanced if:
- Any left parenthesis '(' must have a corresponding two consecutive right parenthesis '))'.
- Left parenthesis '(' must go before the corresponding two consecutive right parenthesis '))'.

In other words, we treat '(' as an opening parenthesis and '))' as a closing parenthesis.
- For example, "())", "())(())))" and "(())())))" are balanced, ")()", "()))" and "(()))" are not balanced.

You can insert the characters '(' and ')' at any position of the string to balance it if needed.
Return the minimum number of insertions needed to make s balanced.

EXAMPLE 1:
Input: s = "(()))"
Output: 1
Explanation: The second '(' has two matching '))', but the first '(' has only ')' matching.
We need to add one more ')' at the end of the string to be "(())))" which is balanced.

EXAMPLE 2:
Input: s = "())"
Output: 0
Explanation: The string is already balanced.

EXAMPLE 3:
Input: s = "))())("
Output: 3
Explanation: Add '(' to match the first '))', Add '))' to match the last '('.

CONSTRAINTS:
- 1 <= s.length <= 105
- s[i] is either '(' or ')'.
- s is a valid parentheses string.
"""


class Solution:
    @staticmethod
    def minInsertions(s: str) -> int:
        balance = 0
        insertions = 0
        index = 0

        while index < len(s):
            if s[index] == "(":
                balance += 1
                index += 1
            else:
                if index + 1 < len(s) and s[index + 1] == ")":
                    index += 2
                else:
                    # Complete the lone ')' into a consecutive pair.
                    insertions += 1
                    index += 1

                if balance > 0:
                    balance -= 1
                else:
                    # This closing pair needs an opening before it.
                    insertions += 1

        return insertions + 2 * balance


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.minInsertions("(()))")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.minInsertions("())")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.minInsertions("))())(")
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.minInsertions(")))))))")
    print(f"CASE 4 Result: {result4}")

    # Printing blank line seperator
    print()

    # CASE 5
    result5 = solution.minInsertions("()())))()")
    print(f"CASE 5 Result: {result5}")

    # Printing blank line seperator
    print()

    # CASE 6
    result6 = solution.minInsertions("))(()()))()))))))()())()(())()))))()())(()())))()(")
    print(f"CASE 6 Result: {result6}")
