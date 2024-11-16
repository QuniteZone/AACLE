from function import Complexity_Analysis_Phase
import os

api_key = "sk-Oq5AQr83cGogeQ0TXzdN7uEcI7PwhBNQ0YQ8woWECLLQ406C"
os.environ["OPENAI_API_KEY"] = api_key

input = """
function quicksort(array, low, high)
    if low < high then
        // Partition the array and get the pivot index
        pivot_index = partition(array, low, high)
        
        // Recursively sort elements before and after partition
        quicksort(array, low, pivot_index - 1)
        quicksort(array, pivot_index + 1, high)
    end if
end function

function partition(array, low, high)
    // Choose the rightmost element as pivot
    pivot = array[high]
    i = low - 1
    
    for j = low to high - 1 do
        if array[j] <= pivot then
            i = i + 1
            swap array[i] and array[j]
        end if
    end for
    
    // Swap the pivot element with the element at i+1
    swap array[i + 1] and array[high]
    
    return i + 1
end function

function swap(a, b)
    temp = a
    a = b
    b = temp
end function
"""

complexity_analysis_phase = Complexity_Analysis_Phase("gpt-3.5-turbo", "output_Files")
complexity_analysis_phase.phase_run(input)
