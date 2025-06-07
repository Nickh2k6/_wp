def classify_even_odd(numbers):
    result = {
        'even': [num for num in numbers if num % 2 == 0],
        'odd': [num for num in numbers if num % 2 != 0]
    }
    return result

# 測試範例
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(classify_even_odd(numbers))