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

def recursive_reverse_engineer(how_many, mean0, stddev0, median0, chosen_a, chosen_b, results):
    required_sum = round(mean0 * how_many)
    missing_sum = required_sum - median0 - sum(chosen_a) - sum(chosen_b)
    seg_length = how_many // 2

    if len(chosen_b) == seg_length - 1:
        f = missing_sum
        proposed = (chosen_a + [median0,] + chosen_b + [f,])
        # print(proposed, stddev(proposed), stddev0)
        if f in range(chosen_b[-1], 101) and stddev(proposed) == stddev0:
            results.append(proposed)
        return

    try_min = 0
    try_max = 0
    if len(chosen_a) < seg_length:
        if len(chosen_a) > 0:
            try_min += chosen_a[-1] * (seg_length - len(chosen_a))
        try_max += median0 * (seg_length - len(chosen_a))
    try_min += median0 * (seg_length - len(chosen_b))
    try_max += 100 * (seg_length - len(chosen_b))

    if try_min > missing_sum or try_max < missing_sum:
        return

    if len(chosen_a) != seg_length:
        start = 1
        if len(chosen_a) > 0:
            start = chosen_a[-1]

        end = median0

        for x in range(start, end+1):
            recursive_reverse_engineer(how_many, mean0, stddev0, median0, chosen_a + [x,], chosen_b, results)
    else:
        end = 100
        start = median0
        if len(chosen_b) > 0:
            start = chosen_b[-1]

        for x in range(start, end+1):
            recursive_reverse_engineer(how_many, mean0, stddev0, median0, chosen_a, chosen_b + [x,], results)

    return results


x = stats([1,2,3,4,5])
print(x)
print(recursive_reverse_engineer(5, x[0], x[1], x[2], [], [], []))

x = stats([94, 97, 98, 99, 99])
print(recursive_reverse_engineer(5, x[0], x[1], x[2], [], [], []))

x = stats([42, 50, 58, 58, 71, 76, 86])
# (63.0, 14.252819269985048, 58)
print(recursive_reverse_engineer(7, x[0], x[1], x[2], [], [], []))

N = 7
while True:
    import random
    # Generate N random numbers
    randomN = [random.randint(0, 100) for x in range(N)]
    # Ensure mean is > 60
    if sum(randomN) < 60*N: continue
    sN = sorted(randomN)
    x = stats(sN)
    rNs = recursive_reverse_engineer(N, x[0], x[1], x[2], [], [], [])
    print(sN, stats(sN))
    for rN in rNs:
        print(rN, stats(rN))
    print("number of matches:", len(rNs))
    assert sN in rNs
