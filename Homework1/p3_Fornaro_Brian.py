# -*- coding: utf-8 -*-
def find_dup_str(s, n):
    for i in range(len(s) - n + 1):
        substring = s[i:i + n]

        for j in range(i + n, len(s) - n + 1):
            if substring == s[j:j + n]:
                return substring

    return ""


def find_max_dup(s):
    longest = ""

    for n in range(1, len(s) // 2 + 1):
        result = find_dup_str(s, n)

        if result != "":
            longest = result

    return longest


s = input("Enter a string: ")
n = int(input("Enter n: "))
print(find_dup_str(s, n))

s = input("Enter a string: ")
print(find_max_dup(s))

