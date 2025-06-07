def most_common(nums):
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
    # 找出次數最多的數字
    max_count = max(count.values())
    for key, value in count.items():
        if value == max_count:
            return key

# 測試範例
nums = [1, 2, 2, 3, 3, 3, 4]
print(most_common(nums))  # 輸出: 3