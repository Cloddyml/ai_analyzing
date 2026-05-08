#include <stdio.h>

int main(void) {
    int arr[10] = {0};
    int *p = arr + sizeof(int) * 5;
    *p = 42;
    printf("%d\n", *p);
    return 0;
}
