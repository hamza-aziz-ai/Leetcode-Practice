"""
Given a string s containing only three types of characters: '(', ')' and '*', return true if s is valid.
The following rules define a valid string:
- Any left parenthesis '(' must have a corresponding right parenthesis ')'.
- Any right parenthesis ')' must have a corresponding left parenthesis '('.
- Left parenthesis '(' must go before the corresponding right parenthesis ')'.
- '*' could be treated as a single right parenthesis ')' or a single left parenthesis '(' or an empty string "".

EXAMPLE 1:
Input: s = "()"
Output: true

EXAMPLE 2:
Input: s = "(*)"
Output: true

EXAMPLE 3:
Input: s = "(*))"
Output: true

CONSTRAINTS:
- 1 <= s.length <= 100
- s[i] is '(', ')' or '*'.
"""


class Solution:
    @staticmethod
    def checkValidString(s: str) -> bool:
        low = high = 0

        for char in s:
            if char == "(":
                low += 1
                high += 1
            elif char == ")":
                low -= 1
                high -= 1
            else:  # "*"
                low -= 1
                high += 1

            if high < 0:
                return False

            low = max(low, 0)

        return low == 0


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.checkValidString("()")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.checkValidString("(*)")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.checkValidString("(*))")
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.checkValidString("(")
    print(f"CASE 4 Result: {result4}")

    # Printing blank line seperator
    print()

    # CASE 5
    result5 = solution.checkValidString("((((()(()()()*()(((((*)()*(**(())))))(())()())(((())())())))))))(((((())*)))()))(()((*()*(*)))(*)()")
    print(f"CASE 5 Result: {result5}")

    # Printing blank line seperator
    print()

    # CASE 6
    result6 = solution.checkValidString("(((((*(()((((*((**(((()()*)()()()*((((**)())*)*)))))))(())(()))())((*()()(((()((()*(())*(()**)()(())")
    print(f"CASE 6 Result: {result6}")

    # Printing blank line seperator
    print()

    # CASE 7
    result7 = solution.checkValidString(")(")
    print(f"CASE 7 Result: {result7}")
