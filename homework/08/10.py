def summary(data):
    for student in data:
        name = student['name']
        scores = student['scores']
        total = sum(scores)
        average = total / len(scores)
        print(f"學生: {name}, 總分: {total}, 平均: {average:.2f}")

# 測試範例
students = [
    {'name': 'Alice', 'scores': [90, 80, 70]},
    {'name': 'Bob', 'scores': [100, 85, 95]}
]

summary(students)