def bubbuleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


nums = [5, 3, 2, 1, 4]
bubbuleSort(nums)
print(nums)
