def average(nums):
    avg = sum(nums)/len(nums)
    return round(avg, 1)
print(average([1,5,8,9,6,14]))