def func(n):
    result = ''
    i = 1
    while len(result) < n:
        result += str(i) * i
        i += 1
    return result[:n]


print(func(6))