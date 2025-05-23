def find_max(numbers):
    if not numbers:
        return None
    maxnum = numbers[0]

    for num in numbers:
        if num > maxnum:
            maxnum = num
    return maxnum
print(find_max([1,5,8,6,9]))