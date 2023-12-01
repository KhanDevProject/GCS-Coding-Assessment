#include <stdio.h>

// Function to perform bubble sort on the 'numbers' array
void sort(float numbers[], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (numbers[j] > numbers[j + 1]) {
                // Swap if the current element is greater than the next element
                float temp = numbers[j];
                numbers[j] = numbers[j + 1];
                numbers[j + 1] = temp;
            }
        }
    }
}

// Function to find the median of the 'numbers' array
float sort_and_find_median(float numbers[], int n) {
    // Call the sort function to sort the input numbers
    sort(numbers, n);
    
    // Check if the length is even
    if (n % 2 == 0) {
        // If even, calculate the median as the average of the middle two numbers
        return (numbers[n / 2 - 1] + numbers[n / 2]) / 2;
    } else {
        // If odd, the median is the middle number
        return numbers[n / 2];
    }
}

int main() {
    
    // OPTION 1: inputting the array of numbers
    // UNCOMMENT TO TEST THIS CASE 
    /* 
    // Get user input for the number of elements
    printf("Enter the number of elements: ");
    int array_length;
    scanf("%d", &array_length);

    // Get user input for the array elements
    float numbers[array_length];
    printf("Enter %d numbers separated by spaces: ", array_length);
    for (int i = 0; i < array_length; i++) {
        scanf("%f", &numbers[i]);
    }

    // Call the sort_and_find_median function and print the result
    float result = sort_and_find_median(numbers, array_length);
    printf("Median: %.1f\n", result);
*/ 

    // OPTION 2: Predefined test cases 
    
    // Provide an array of numbers for testing
    float test_array[] = { 9, 10,2};

    // Calculate the length of the array
    int array_length = sizeof(test_array) / sizeof(test_array[0]);

    // Call the sort_and_find_median function and print the result
    float result = sort_and_find_median(test_array, array_length);
    printf("Median: %.1f\n", result);
    return 0;
}
