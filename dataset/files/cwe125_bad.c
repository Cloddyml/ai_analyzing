#include <stdio.h>

#define SIZE 5

int main() {
    int arr[SIZE] = {1, 2, 3, 4, 5};
    int idx = SIZE + 2;
    printf("%d\n", arr[idx]);
    return 0;
}
