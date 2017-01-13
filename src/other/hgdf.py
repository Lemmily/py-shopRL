
import sys, math


def allnumbers(num):
    the_numbers = []
    for i in range(0, len(num)):
        the_numbers.append(num[i])
    list_nums = [num]
    for ix in range(len(the_numbers)):
        x = the_numbers[ix]
        orig_key = "" + x
        key = orig_key
        list_nums.append(key)

        for iy in range(ix + 1, len(the_numbers)):
            key = orig_key
            for iz in range(iy + 1, len(the_numbers)):
                y = the_numbers[iz]
                key += y
                list_nums.append(key)
            key = orig_key
            key += the_numbers[iy]
            list_nums.append(key)

    return list_nums

n = 3  # int(input().strip())
number = '968'  # input().strip()
count = 0
if 1 <= n and n <= 2 + 2 * math.pow(10,5):
    numbers = allnumbers(number)
    for a in numbers:
        if int(a) % 8 == 0:
            count += 1

    print (int(count % (math.pow(10, 9) + 7)))

    # print (int(3 % (math.pow(10, 9) + 7)))