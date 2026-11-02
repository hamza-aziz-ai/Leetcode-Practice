"""
A valid parentheses string is either empty "", "(" + A + ")", or A + B, where A and B are valid parentheses strings, and + represents string concatenation.

- For example, "", "()", "(())()", and "(()(()))" are all valid parentheses strings.

A valid parentheses string s is primitive if it is nonempty, and there does not exist a way to split it into s = A + B, with A and B nonempty valid parentheses strings.

Given a valid parentheses string s, consider its primitive decomposition: s = P1 + P2 + ... + Pk, where Pi are primitive valid parentheses strings.

Return s after removing the outermost parentheses of every primitive string in the primitive decomposition of s.

EXAMPLE 1:
Input: s = "(()())(())"
Output: "()()()"
Explanation:
The input string is "(()())(())", with primitive decomposition "(()())" + "(())".
After removing outer parentheses of each part, this is "()()" + "()" = "()()()".

EXAMPLE 2:
Input: s = "(()())(())(()(()))"
Output: "()()()()(())"
Explanation:
The input string is "(()())(())(()(()))", with primitive decomposition "(()())" + "(())" + "(()(()))".
After removing outer parentheses of each part, this is "()()" + "()" + "()(())" = "()()()()(())".

EXAMPLE 3:
Input: s = "()()"
Output: ""
Explanation:
The input string is "()()", with primitive decomposition "()" + "()".
After removing outer parentheses of each part, this is "" + "" = "".

CONSTRAINTS:
- 1 <= s.length <= 105
- s[i] is either '(' or ')'.
- s is a valid parentheses string.
"""


class Solution:
    @staticmethod
    def removeOuterParentheses(s: str) -> str:
        result = ""

        ## FIRST APPROACH
        # pairs = dict()
        # for i, character in enumerate(s):
        #     if character == ")":
        #         pairs[next((k for k, v in reversed(pairs.items()) if v is None), None)] = i
        #         continue
        #
        #     pairs[i] = None
        #
        # print(pairs)
        # print()
        #
        # key, value = list(pairs.items())[0]
        # outer_most = dict()
        # while value != len(s):
        #     value = pairs[key]
        #     outer_most[key] = value
        #     value += 1
        #     key = value
        #
        # outer_most_index_tuple = list(outer_most.items())
        # print(outer_most_index_tuple)
        #
        # for pair in outer_most_index_tuple:
        #     start, end = pair
        #     result += s[start+1:end]
        #     print(result)

        ## SECOND APPROACH
        # balance = 0
        # index = 0
        #
        # for i, character in enumerate(s):
        #     if character == "(":
        #         balance += 1
        #     elif character == ")":
        #         balance -= 1
        #
        #     if balance == 0:
        #         result += s[index+1:i]
        #         index = i + 1

        ## THIRD APPROACH
        balance = 0
        index = 0

        decomposed_parentheses_list = list()

        for i, character in enumerate(s):
            if character == "(":
                balance += 1
            elif character == ")":
                balance -= 1

            if balance == 0:
                decomposed_parentheses_list.append(s[index+1:i])
                index = i + 1

        result = result.join(decomposed_parentheses_list)

        return result


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.removeOuterParentheses("(()())(())")
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.removeOuterParentheses("(()())(())(()(()))")
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.removeOuterParentheses("()()")
    print(f"CASE 3 Result: {result3}")
