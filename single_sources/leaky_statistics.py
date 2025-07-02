"""
there are 7 students in a computer class; there is a test and the teacher
published a set of statistics the mean median and stddev of the scores this
inadvertantly leaked the score of the students since the number of students was
so small write a function to reverse engineer the scores assuming they are
integers between 0-100

The mean and stddev are considered a match if they are within error of 0.01 <--- ehh, apparently stddev of samples are so much easier to overlap...


Result: after writing the program, it looks like that the number of candidate solutions are much greater than I expected.
"""

import math
import collections

def mean(numbers):
    return sum(numbers) / len(numbers)

def stddev(numbers):
    if len(numbers) == 0:
        return 0
    mean_val = mean(numbers)
    return math.sqrt(sum((x - mean_val)*(x - mean_val) for x in numbers) / len(numbers))

def median(numbers):
    n = len(numbers)
    if n % 2 == 1:
        return numbers[n // 2]
    else:
        return numbers[n // 2] + numbers[n // 2 - 1] / 2

def stats(numbers):
    return (mean(numbers), stddev(numbers), median(numbers))

def reverse_engineer(mean0, stddev0, median0):
    required_sum = round(mean0 * 7)

    candidates = []

    for a in range(0, median0+1):
        missing_sum = required_sum - median0 - a
        if 2 * median0 + 3 * 100 < missing_sum: continue
        if 2 * a + 3 * median0 > missing_sum: break

        for b in range(a, median0+1):
            missing_sum = required_sum - median0 - a - b
            if 1 * median0 + 3 * 100 < missing_sum: continue
            if 1 * b + 3 * median0 > missing_sum: break

            for c in range(b, median0+1):
                missing_sum = required_sum - median0 - a - b - c
                if 3 * 100 < missing_sum: continue
                if 3 * median0 > missing_sum: break

                for d in range(median0, 101):
                    missing_sum = required_sum - median0 - a - b - c - d
                    if 2 * 100 < missing_sum: continue
                    if 2 * d > missing_sum: break

                    for e in range(d, 101):
                        # print(a,b,c,d,e)
                        f = required_sum - median0 - a - b - c - d - e
                        if f not in range(0, 101): continue

                        proposed = [a,b,c,median0,d,e,f]
                        if stddev(proposed) == stddev0:
                            assert (mean(proposed) - mean0) < 0.00001
                            candidates.append(sorted(proposed))

    return candidates

x = stats([1,2,3,4,5,6,7])
print(x)
print(reverse_engineer(x[0], x[1], x[2]))

x = stats([94, 97, 98, 98, 98, 99, 99])
print(reverse_engineer(x[0], x[1], x[2]))

while True:
    import random
    # Generate 7 random numbers
    random7 = [random.randint(0, 100) for x in range(7)]
    # Ensure mean is > 60
    if sum(random7) < 60*7: continue
    s7 = sorted(random7)
    x = stats(s7)
    r7s = reverse_engineer(x[0], x[1], x[2])
    print(s7, stats(s7))
    for r7 in r7s:
        print(r7, stats(r7))
    print("number of matches:", len(r7s))
    assert s7 in r7s
