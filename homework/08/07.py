def dict_to_string(d):
    return ", ".join(f"{key}:{value}" for key, value in d.items())

# 測試範例
example_dict = {'a': 1, 'b': 2}
print(dict_to_string(example_dict))  # 輸出: "a:1, b:2"