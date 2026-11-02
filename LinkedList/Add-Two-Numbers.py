"""
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.

EXAMPLE 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

EXAMPLE 2:
Input: l1 = [0], l2 = [0]
Output: [0]

EXAMPLEe 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

CONSTRAINTS:
- The number of nodes in each linked list is in the range [1, 100].
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros.
"""

from LinkedList import ListNode

# class Solution:
#     @staticmethod
#     def addTwoNumbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
#         currentNode1 = l1
#         string1 = str(currentNode1.val)
#         while currentNode1.next is not None:
#             currentNode1 = currentNode1.next
#             string1 += str(currentNode1.val)
#
#         currentNode2 = l2
#         string2 = str(currentNode2.val)
#         while currentNode2.next is not None:
#             currentNode2 = currentNode2.next
#             string2 += str(currentNode2.val)
#
#         string1, string2 = string1[::-1], string2[::-1]
#
#         num1, num2 = int(string1), int(string2)
#
#         sumString = str(num1 + num2)
#
#         sumString = sumString[::-1]
#
#         print(sumString)
#
#         sumLinkedList = ListNode()
#         current_node = sumLinkedList
#         i = 0
#         current_node.val = int(sumString[i])
#         while i < len(sumString) - 1:
#             i += 1
#             current_node.next = ListNode(int(sumString[i]))
#             current_node = current_node.next
#
#         return sumLinkedList

class Solution:
    @staticmethod
    def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
        def reverse_linked_list(linked_list: ListNode) -> ListNode:
            # Reverse Linked List
            head_node = linked_list
            if head_node.next is None:
                reversed_linked_list = linked_list
            else:
                previous_node = head_node
                current_node = head_node.next
                previous_node.next = None
                while current_node is not None:
                    # Perform reverse
                    next_node = current_node.next
                    current_node.next = previous_node
                    previous_node = current_node
                    current_node = next_node

                reversed_linked_list = previous_node

            return reversed_linked_list

        reversed_l1 = reverse_linked_list(l1)
        reversed_l2 = reverse_linked_list(l2)

        currentNode1 = reversed_l1
        currentNode2 = reversed_l2
        sumLinkedList = ListNode()
        current_node = sumLinkedList
        carry_over = 0

        while current_node is not None:
            sum = currentNode1.val + currentNode2.val + carry_over
            currentNode1 = currentNode1.next
            currentNode2 = currentNode2.next

            if sum > 10:
                sumString = str(sum)
                current_node.val = int(sumString[1])
                carry_over = int(sumString[0])
            else:
                current_node.val = sum

            current_node = current_node.next

            if currentNode1 is None or currentNode2 is None:
                break

        return reverse_linked_list(sumLinkedList)




if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    l1 = ListNode(2, ListNode(4, ListNode(3)))
    l2 = ListNode(5, ListNode(6, ListNode(4)))
    result1 = solution.addTwoNumbers(l1, l2)
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    l1 = ListNode(0)
    l2 = ListNode(0)
    result2 = solution.addTwoNumbers(l1, l2)
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    l1 = ListNode(9,
                  ListNode(9,
                           ListNode(9,
                                    ListNode(9,
                                             ListNode(9,
                                                      ListNode(9,
                                                               ListNode(9)
                                                               )
                                                      )
                                             )
                                    )
                           )
                  )
    l2 = ListNode(9,
                  ListNode(9,
                           ListNode(9,
                                    ListNode(9)
                                    )
                           )
                  )
    result3 = solution.addTwoNumbers(l1, l2)
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    l1 = ListNode(0)
    l2 = ListNode(1)
    result4 = solution.addTwoNumbers(l1, l2)
    print(f"CASE 4 Result: {result4}")
