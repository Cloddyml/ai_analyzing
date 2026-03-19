#include <stdio.h>
#include <stdlib.h>

int get_value(int *ptr) {
    if (ptr == NULL) return -1;
    return *ptr;
}

int main() {
    int val = 42;
    printf("%d\n", get_value(&val));
    return 0;
}
