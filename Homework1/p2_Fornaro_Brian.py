# -*- coding: utf-8 -*-
def find_Pythagorean(n):
    triples = []

    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a ** 2 + b ** 2 == c ** 2:
                    triples.append((a, b, c))

    return triples


n = int(input("Enter n: "))

triples = find_Pythagorean(n)

for triple in triples:
    print(triple)
    
