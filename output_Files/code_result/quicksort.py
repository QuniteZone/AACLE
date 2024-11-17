# filename: quicksort.py

def quicksort(array, low, high):
    if low < high:
        # Partition the array and get the pivot index
        pivot_index = partition(array, low, high)

        # Recursively sort elements before and after partition
        quicksort(array, low, pivot_index - 1)
        quicksort(array, pivot_index + 1, high)

def partition(array, low, high):
    # Choose the rightmost element as pivot
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            array[i], array[j] = array[j], array[i]

    # Swap the pivot element with the element at i+1
    array[i + 1], array[high] = array[high], array[i + 1]

    return i + 1

def swap(a, b):
    temp = a
    a = b
    b = temp

# Example usage
arr = [29, 10, 14, 37, 13]
quicksort(arr, 0, len(arr) - 1)
print(arr)