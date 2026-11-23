#!/bin/python3
# HackerRank: FizzBuzz
#
# For every i from 1 to n print FizzBuzz if i is divisible by both 3 and 5,
# Fizz if only by 3, Buzz if only by 5, and i otherwise. One result per line.
#
# The order of the tests matters: check "both" first. If the "divisible by 3"
# test came first, 15 would print Fizz and never reach the FizzBuzz branch.
# i % 3 == 0 means "3 goes into i with nothing left over".


def fizzBuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


if __name__ == '__main__':
    n = int(input().strip())

    fizzBuzz(n)
