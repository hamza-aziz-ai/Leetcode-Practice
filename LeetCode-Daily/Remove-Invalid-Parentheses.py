"""
Given a string s that contains parentheses and letters, remove the minimum number of invalid parentheses to make the input string valid.
Return a list of unique strings that are valid with the minimum number of removals. You may return the answer in any order.

EXAMPLE 1:
Input: s = "()())()"
Output: ["(())()","()()()"]

EXAMPLE 2:
Input: s = "(a)())()"
Output: ["(a())()","(a)()()"]

EXAMPLE 3:
Input: s = ")("
Output: [""]

CONSTRAINTS:
- 1 <= s.length <= 25
- s consists of lowercase English letters and parentheses '(' and ')'.
- There will be at most 20 parentheses in s.
"""


class Solution:
    @staticmethod
    def removeInvalidParentheses(s: str) -> list[str]:
        candidates = {s}

        def check_validity(candidates):
            valid_candidates = []

            for candidate in candidates:
                balance = 0
                for character in candidate:
                    if character == "(":
                        balance += 1
                    elif character == ")":
                        balance -= 1
                        if balance < 0:
                            break

                if balance == 0:
                    valid_candidates.append(candidate)

            return valid_candidates

        while True:
            valid_candidates = check_validity(candidates)

            if valid_candidates:
                return valid_candidates

            next_candidates = set()

            for candidate in candidates:
                for i, character in enumerate(candidate):
                    if character in ["(", ")"]:
                        new_string = candidate[:i] + candidate[i+1:]
                        next_candidates.add(new_string)

            candidates = next_candidates


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.removeInvalidParentheses("()())()")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.removeInvalidParentheses("(a)())()")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.removeInvalidParentheses(")(")
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.removeInvalidParentheses("n")
    print(f"CASE 4 Result: {result4}")

    # Printing blank line seperator
    print()

    # CASE 5
    result5 = solution.removeInvalidParentheses(")(f")
    print(f"CASE 5 Result: {result5}")
