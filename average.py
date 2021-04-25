def average(array):
    x = 0;
    y = 0;
    for i in range(len(array)):
        x = x + array[i]
        y = i + 1
    return x / y;

