def func(n):
    result = ''
    i = 1
    while len(result) < n:
        result += str(i) * i
        i += 1
    return result[:n]


if __name__ == '__main__':
    number = int(input("Введите количество элементов последовательности: "))
    print(f"Результат: {func(number)}")
