#include <stdio.h>

int get_element(int *arr, int size, int idx) {
    if (idx < 0 || idx >= size) return -1;
    return arr[idx];
}

int main(void) {
    int data[5] = {1, 2, 3, 4, 5};
    int idx = -1;
    printf("%d\n", get_element(data, 5, idx));
    return 0;
}
