def sort_and_find_median(numbers):
    # Call the bubble_sort function to sort the input numbers
    sort(numbers)
    
    # Calculate the length of the sorted numbers list
    n = len(numbers)
    
    # Check if the length is even
    if n % 2 == 0:
        # If even, calculate the median as the average of the middle two numbers
        median = (numbers[int(n / 2) - 1] + numbers[int(n / 2)]) / 2
    else:
        # If odd, the median is the middle number
        median = numbers[int(n / 2)]
    
    # Return the calculated median value
    return median

def sort(numbers):
    # Get the length of the input array
    array_length = len(numbers)
    # Iterate through each element of the array
    for current_pass in range(array_length):
        # The last current_pass elements are already sorted, so no need to check them
        # Iterate through the unsorted part of the array
        for current_index in range(0, array_length - current_pass - 1):
            # Swap if the current element is greater than the next element
            if numbers[current_index] > numbers[current_index + 1]:
                # Swap the elements using a temporary variable
                numbers[current_index], numbers[current_index + 1] = numbers[current_index + 1], numbers[current_index]


# Get user input for a list of numbers
user_input = input("Enter a list of numbers separated by spaces: ")
numbers = list(map(float, user_input.split()))

# Call the sort_and_find_median function and print the result
result = sort_and_find_median(numbers)
print(f"Median: {result}")
