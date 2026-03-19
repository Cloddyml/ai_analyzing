#include <stdio.h>

#define SIZE 5

int safe_get(int *arr, int size, int idx) {
    if (idx < 0 || idx >= size) return -1;
    return arr[idx];
}

int main() {
    int arr[SIZE] = {1, 2, 3, 4, 5};
    printf("%d\n", safe_get(arr, SIZE, 3));
    return 0;
}
