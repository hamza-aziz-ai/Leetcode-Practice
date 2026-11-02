"""
You are given a 0-indexed integer array nums and a positive integer k.

You can do the following operation on the array any number of times:
- Choose any two distinct indices i and j and simultaneously update the values of nums[i] to (nums[i] AND nums[j]) and nums[j] to (nums[i] OR nums[j]). Here, OR denotes the bitwise OR operation, and denotes the bitwise AND operation.

You have to choose k elements from the final array and calculate the sum of their squares.

Return the maximum sum of squares you can achieve.

Since the answer can be very large, return it modulo 109 + 7.

EXAMPLE 1:
Input: nums = [2,6,5,8], k = 2
Output: 261
Explanation: We can do the following operations on the array:
- Choose i = 0 and j = 3, then change nums[0] to (2 AND 8) = 0 and nums[3] to (2 OR 8) = 10. The resulting array is nums = [0,6,5,10].
- Choose i = 2 and j = 3, then change nums[2] to (5 AND 10) = 0 and nums[3] to (5 OR 10) = 15. The resulting array is nums = [0,6,0,15].
We can choose the elements 15 and 6 from the final array. The sum of squares is 152 + 62 = 261.
It can be shown that this is the maximum value we can get.

EXAMPLE 2:
Input: nums = [4,5,4,7], k = 3
Output: 90
Explanation: We do not need to apply any operations.
We can choose the elements 7, 5, and 4 with a sum of squares: 72 + 52 + 42 = 90.
It can be shown that this is the maximum value we can get.

CONSTRAINTS:
- 1 <= k <= nums.length <= 105
- 1 <= nums[i] <= 109
"""
from collections import Counter
from itertools import zip_longest


# class Solution:
#     @staticmethod
#     def maxSum(nums: list[int], k: int) -> int:
#         nums.sort()
#         maximum_bit_length = nums[-1].bit_length()
#         binary_numbers = list()
#
#         for num in nums:
#             binary_form = list(bin(num).split('b')[1])
#             binary_form = [int(bit) for bit in binary_form]
#             int_binary_form = [0] * (maximum_bit_length - len(binary_form)) + binary_form
#             binary_numbers.append(int_binary_form)
#
#         bit_worth_occurrences = dict()
#
#         for i, bits in enumerate(zip(*binary_numbers)):
#             bit_worth_occurrences[2 ** (maximum_bit_length - i - 1)] = sum(bits)
#
#         groups = [[bit_worth] * available_occerences for bit_worth, available_occerences in bit_worth_occurrences.items()]
#
#         bit_worth_list = [[x for x in layer if x is not None] for layer in zip_longest(*groups)]
#
#         largest_possible_numbers = list()
#         for combination in bit_worth_list:
#             largest_possible_numbers.append(sum(combination))
#
#         largest_possible_numbers.sort(reverse=True)
#
#         max_sum = 0
#         for number in largest_possible_numbers[:k]:
#             max_sum += (number ** 2)
#
#         return max_sum % ((10 ** 9) + 7)

class Solution:
    @staticmethod
    def maxSum(nums: list[int], k: int) -> int:
        counts = [0] * 32

        for number in nums:
            for bit in range(32):
                counts[bit] += (number >> bit) & 1

        answer = 0

        for rank in range(k):
            value = 0

            for bit in range(32):
                if counts[bit] > rank:
                    value |= 1 << bit

            answer = (answer + value * value) % (10**9 + 7)

        return answer


if __name__ == "__main__":
    solution = Solution()

    # CASE 1
    result1 = solution.maxSum(nums = [2,6,5,8], k = 2)
    print(f"CASE 1 Result: {result1}")

    # Printing blank line seperator
    print()

    # CASE 2
    result2 = solution.maxSum(nums = [4,5,4,7], k = 3)
    print(f"CASE 2 Result: {result2}")

    # Printing blank line seperator
    print()

    # CASE 3
    result3 = solution.maxSum(nums = [32,85,61], k = 1)
    print(f"CASE 3 Result: {result3}")

    # Printing blank line seperator
    print()

    # CASE 4
    result4 = solution.maxSum(
        nums = [420,1831,628,923,1956,1507,1426,223,454,584,1299,1950,603,1502,1326,349,764,1882,609,526,181,1649,882,1049,143,1887,1035,1159,67,1817,721,1813,1398,1484,982,1186,1333,1906,1196,845,948,1351,1274,1483,121,1074,18,1610,328,1885,1038,1345,1400,564,1235,1859,1469,245,1589,1380,110,417,1488,823,634,1936,617,578,400,824,1935,1688,550,301,407,1532,1910,933,735,1888,953,1105,233,973,1518,931,118,9,119,1346,698,727,254,1295,1495,1167,597,1,63,335,1550,363,1849,1211,1324,1723,1069,441,1781,1726,1387,862,1207,397,47,535,1078,140,1527,1749,1061,1750,1103,814,968,570,1993,671,1538,1757,709,233,1288,1293,232,1234,1450,161,166,1395,587,89,1549,671,147,1141,341,206,788,56,300,840,666,1677,1060,1268,1568,1378,1793,1259,1064,1652,622,222,608,1671,1435,1293,1976,1315,620,1208,651,324,703,1315,1382,1405,1156,979,692,52,336,1472,620,1347,465,1116,734,326,1614,860,1598,301,1193,749,915,613,66,1680,1785,1545,1087,60,1924,52,881,1985,2,1228,1613,1676,513,1557,431,1097,1266,338,1268,59,676,760,250,1556,1005,504,69,864,1256,892,1066,1965,1076,926,1432,1504,628,1429,371,88,137,1706,1879,1119,1673,1408,401,1123,1414,1280,145,101,12,305,738,233,1188,1052,1104,889,541,1839,1413,1892,653,443,36,1549,1776,1954,275,1630,1815,1812,1953,1806,1611,245,696,1155,1035,1841,1232,941,1423,1335,89,955,424,469,1643,1399,1723,1012,1120,109,1894,1435,1450,1794,1146,113,1651,642,1168,479,30,423,44,446,66,1719,30,826,963,937,19,1907,876,375,202,1716,579,1426,582,1992,754,332,706,1962,1558,1086,142,756,1343,1957,373,759,274,11,1859,725,1206,1196,783,1190,1916,471,583,1935,1252,1840,1030,1090,902,426,999,211,244,1878,325,1411,1944,1308,1836,32,26,1135,467,77,1632,999,158,268,752,1750,1853,504,805,1945,696,1379,66,354,464,860,328,1977,64,136,300,1399,761,162,1934,62,1087,344,1399,1155,815,898,1575,1864,805,1538,899,1900,1624,1969,1201,1957,1153,1498,351,820,1718,1568,521,1081,251,1203,1956,951,842,1672,376,1189,610,357,1495,1988,676,337,1471,489,92,509,870,1326,1928,1718,589,376,1082,758,1465,1016,1614,1706,1538,605,485,1532,355,1758,946,1158,571,1396,1320,1275,1142,1717,933,1585,224,1619,629,704,1657,1752,311,140,937,882,1441,990,1465,148,71,256,1865,82,1622,1188,461,3,831,1922,1762,230,325,333,1898,371,1974,1024,255,303,1016,161,1136,1206,72,701,169,1692,1454,1119,115,599,639,456,1154,952,629,1913,362,876,1464,289,1883,375,1224,1990,1352,1980,936,1849,90,1561,2,600,117,1359,1069,1720,26,2,1413,643,1147,767,1387,1203,1452,1477,1206,98,76,170,1122,466,1062,1341,1006,674,1617,1708,1718,1906,925,1404,1861,1219,1585,1496,78,71,642,1105,1637,1154,239,911,980,854,551,1163,348,1451,1047,1868,1718,95,1569,866,1915,464,609,1186,896,1708,776,1316,1112,1933,1083,1112,717,1747,804,570,1786,1143,1144,1001,295,1123,1121,1176,1512,929,1542,1624,1041,1360,857,1817,1760,839,1561,138,896,610,914,379,901,527,653,969,1356,96,866,457,1090,379,476,958,1594,175,425,30,794,1405,1772,33,1059,1546,386,973,1060,673,712,1616,880,388,1371,1875,1821,1798,300,985,56,1125,401,917,1204,1765,976,557,522,920,55,1151,1180,823,96,543,7,1862,925,1193,59,1303,1563,236,9,1829,594,1199,1990,1931,1143,1776,1133,682,1291,1487,724,360,565,1945,1654,387,1710,850,1050,1709,1418,811,312,767,1251,1734,1799,203,645,909,101,1746,400,319,317,1262,862,809,398,1857,1362,1652,551,119,1519,1242,1680,702,64,209,880,459,237,332,742,913,293,214,645,491,1060,1526,22,281,280,1506,1069,1327,1697,1085,959,1335,301,1564,1459,1167,904,1715,410,115,1907,96,1999,1622,1013,1011,1517,286,891,31,1214,1185,1405,474,1940,1263,1678,1568,1362,1177,497,1843,733,81,666,1565,1859,1592,1019,348,250,1229,1694,745,214,1013,1698,1612,894,1508,1085,1382,276,1827,1385,862,1828,310,1262,250,99,687,525,1925,1059,918,66,1502,589,1106,1036,1387,1068,111,1279,314,240,1194,1970,1357,691,1695,1024,1827,462,1347,815,847,1799,139,794,197,260,1491,202,1466,955,706,1613,49,1361,255,1753,9,1737,1415,10,475,16,1936,111,94,1445,1094,18,705,813,1576,1091,146,1012,1727,448,1129,1030,1226,934,1762,156,1555,1099,780,35,1678,41,1653,1113,1918,423,1916,517,1091,175,574,1831,190,1022,795,1894,1200,1873,375,886,466,494,1590,1206,1843,5,1611,1496,1971,1640,73,1307,708,1064,1909,766,769,373,1011,85,413,1391,1288,1496,96,976,425,555,120,1645,35,1844,353,1418,1286,84,337,92,1007,706,1609,792,1110,1141,883,30,1342,423,556,403,1568,1731,1053,204,1659,138,91,1481,913],
        k = 545
    )
    print(f"CASE 4 Result: {result4}")
